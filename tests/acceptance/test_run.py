"""`textwerk run` with the group's plug-ins (docs/cli.md)."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import textwerk as tw


class RunTest(tw.ToolTestCase):

    def test_without_plugins_output_is_a_copy(self):
        result = tw.run("run", "--input", tw.SAMPLE, "--output", self.out)
        self.assertExit(result, 0)
        self.assertEqual(self.out.read_bytes(), tw.SAMPLE.read_bytes())

    def test_each_plugin_runs(self):
        """Every plug-in runs alone. From version 2 on, a plug-in that needs
        parameters may end with exit code 5 here instead."""
        names = tw.plugin_names()
        self.assertTrue(names, "no plug-ins listed")
        without_parameters = 0
        for name in names:
            with self.subTest(plugin=name):
                out = self.tmp / f"{name}.txt"
                result = tw.run("run", "--input", tw.SAMPLE, "--output", out, "--plugin", name)
                if result.returncode == 5:
                    self.assertFalse(out.exists(), "output must not be created on error")
                    continue
                self.assertExit(result, 0)
                self.assertTrue(out.exists(), "no output file written")
                out.read_bytes().decode("utf-8")
                without_parameters += 1
        self.assertGreaterEqual(without_parameters, 3,
                                "at least three plug-ins must run without parameters")

    def test_plugins_in_a_chain(self):
        names = [name for name in tw.plugin_names()
                 if tw.run("run", "--input", tw.SAMPLE, "--output", self.tmp / "probe.txt",
                           "--plugin", name).returncode == 0]
        self.assertGreaterEqual(len(names), 3)
        args = []
        for name in names + names[:1]:
            args += ["--plugin", name]
        result = tw.run("run", "--input", tw.SAMPLE, "--output", self.out, *args)
        self.assertExit(result, 0)
        self.assertTrue(self.out.exists(), "no output file written")

    def test_unknown_plugin(self):
        result = tw.run("run", "--input", tw.SAMPLE, "--output", self.out,
                        "--plugin", "no-such-plugin-xyz")
        self.assertExit(result, 3)
        self.assertUserMessage(result, "no-such-plugin-xyz")
        self.assertFalse(self.out.exists(), "output must not be created on error")

    def test_unknown_plugin_after_a_known_one(self):
        names = tw.plugin_names()
        self.assertTrue(names, "no plug-ins listed")
        result = tw.run("run", "--input", tw.SAMPLE, "--output", self.out,
                        "--plugin", names[0], "--plugin", "no-such-plugin-xyz")
        self.assertExit(result, 3)
        self.assertFalse(self.out.exists(), "output must not be created on error")

    def test_existing_output_is_not_changed_on_error(self):
        self.out.write_text("keep me", encoding="utf-8")
        result = tw.run("run", "--input", tw.SAMPLE, "--output", self.out,
                        "--plugin", "no-such-plugin-xyz")
        self.assertExit(result, 3)
        self.assertEqual(self.out.read_text(encoding="utf-8"), "keep me")

    def test_missing_input(self):
        result = tw.run("run", "--input", self.tmp / "missing.txt", "--output", self.out)
        self.assertExit(result, 2)
        self.assertUserMessage(result)
        self.assertFalse(self.out.exists(), "output must not be created on error")


if __name__ == "__main__":
    unittest.main()
