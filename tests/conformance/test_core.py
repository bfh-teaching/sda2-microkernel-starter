"""The core finds plug-ins; it does not know them (docs/cli.md)."""
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import textwerk as tw

CORE = tw.ROOT / "core"
SKIP_DIRS = {"__pycache__", "node_modules", ".git"}
STATIC_IMPORT = re.compile(r"^\s*(from\s+plugins\b|import\s+plugins\b)", re.MULTILINE)


def core_files():
    for path in sorted(CORE.rglob("*")):
        if not path.is_file() or SKIP_DIRS & set(path.parts):
            continue
        if path.name == "README.md" or path.suffix in {".pyc"}:
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue


class CoreConformanceTest(unittest.TestCase):

    def test_core_has_code(self):
        self.assertTrue(list(core_files()), "no source files in core/")

    def test_core_does_not_name_a_plugin(self):
        names = tw.plugin_names()
        self.assertTrue(names, "no plug-ins listed: start with `make test`")
        hits = []
        for path, text in core_files():
            for number, line in enumerate(text.splitlines(), start=1):
                for name in names:
                    if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])", line):
                        hits.append(f"{path.relative_to(tw.ROOT)}:{number}: {name!r}")
        self.assertFalse(hits, "the core names plug-ins:\n" + "\n".join(hits))

    def test_core_does_not_import_plugins_statically(self):
        hits = [str(path.relative_to(tw.ROOT)) for path, text in core_files()
                if STATIC_IMPORT.search(text)]
        self.assertFalse(hits, "static import of plugins in: " + ", ".join(hits))


if __name__ == "__main__":
    unittest.main()
