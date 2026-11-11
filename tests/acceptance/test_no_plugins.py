"""The core works without any plug-in (docs/cli.md, "Where plug-ins come from")."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import textwerk as tw


class NoPluginsTest(tw.ToolTestCase):

    def setUp(self):
        super().setUp()
        self.empty = self.tmp / "empty-plugins"
        self.empty.mkdir()

    def test_list_prints_nothing(self):
        result = tw.run("list", plugins_dir=self.empty)
        self.assertExit(result, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_missing_directory_means_no_plugins(self):
        result = tw.run("list", plugins_dir=self.tmp / "does-not-exist")
        self.assertExit(result, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_run_copies_the_input(self):
        source = self.write_input("Grüezi Frischwerk\n\tZeile 2  \n")
        result = tw.run("run", "--input", source, "--output", self.out, plugins_dir=self.empty)
        self.assertExit(result, 0)
        self.assertEqual(self.out.read_bytes(), source.read_bytes())


if __name__ == "__main__":
    unittest.main()
