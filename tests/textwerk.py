"""Helper for the tests: starts the tool as a user would, from the outside."""
import os
import pathlib
import re
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "shared" / "sample.txt"
FIXTURES = ROOT / "fixtures"
NAME_RE = re.compile(r"^[a-z][a-z0-9-]{2,}$")


def command():
    cmd = os.environ.get("TEXTWERK_CMD")
    if cmd:
        return shlex.split(cmd, posix=(os.name != "nt"))
    return [sys.executable, "-m", "core"]


def run(*args, plugins_dir=None):
    """Run the tool. plugins_dir=None uses the default directory plugins/."""
    env = dict(os.environ)
    env.pop("TEXTWERK_PLUGINS", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if plugins_dir is not None:
        env["TEXTWERK_PLUGINS"] = str(plugins_dir)
    return subprocess.run(
        command() + [str(a) for a in args],
        cwd=ROOT, env=env, capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=60,
    )


def plugin_names(plugins_dir=None):
    """Names from `list`, or [] if the command fails."""
    result = run("list", plugins_dir=plugins_dir)
    if result.returncode != 0:
        return []
    return [line.split("\t")[0] for line in result.stdout.splitlines() if line.strip()]


class ToolTestCase(unittest.TestCase):
    """Gives every test a temporary directory for input and output files."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = pathlib.Path(self._tmp.name)
        self.out = self.tmp / "out.txt"

    def tearDown(self):
        self._tmp.cleanup()

    def write_input(self, text, name="in.txt"):
        path = self.tmp / name
        path.write_bytes(text.encode("utf-8"))
        return path

    def assertExit(self, result, code):
        self.assertEqual(
            result.returncode, code,
            f"expected exit code {code}, got {result.returncode}\n"
            f"stdout: {result.stdout[-500:]}\nstderr: {result.stderr[-500:]}",
        )

    def assertUserMessage(self, result, *needles):
        self.assertTrue(result.stderr.strip(), "expected a message on standard error")
        self.assertNotIn("Traceback", result.stderr, "no stack trace for the user")
        for needle in needles:
            self.assertIn(needle, result.stderr)
