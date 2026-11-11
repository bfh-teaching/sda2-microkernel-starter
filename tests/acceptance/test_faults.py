"""Faulty plug-ins do not stop the core (docs/cli.md, fixtures/README.md)."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import textwerk as tw


class BrokenLoadTest(tw.ToolTestCase):
    """fixtures/broken-load: one working plug-in, one that cannot be loaded."""

    plugins = tw.FIXTURES / "broken-load"

    def test_list_skips_the_broken_plugin_with_a_warning(self):
        result = tw.run("list", plugins_dir=self.plugins)
        self.assertExit(result, 0)
        self.assertTrue(result.stdout.strip(), "the working plug-in must still be listed")
        self.assertUserMessage(result)

    def test_working_plugin_still_runs(self):
        names = tw.plugin_names(self.plugins)
        self.assertTrue(names, "the working plug-in must still be listed")
        result = tw.run("run", "--input", tw.SAMPLE, "--output", self.out,
                        "--plugin", names[0], plugins_dir=self.plugins)
        self.assertExit(result, 0)
        self.assertTrue(self.out.exists(), "no output file written")


class BrokenRunTest(tw.ToolTestCase):
    """fixtures/broken-run: the plug-in `boom` fails when it processes a text."""

    plugins = tw.FIXTURES / "broken-run"

    def test_boom_is_listed(self):
        self.assertIn("boom", tw.plugin_names(self.plugins))

    def test_failing_plugin(self):
        result = tw.run("run", "--input", tw.SAMPLE, "--output", self.out,
                        "--plugin", "boom", plugins_dir=self.plugins)
        self.assertExit(result, 4)
        self.assertUserMessage(result, "boom")
        self.assertFalse(self.out.exists(), "output must not be created on error")


if __name__ == "__main__":
    unittest.main()
