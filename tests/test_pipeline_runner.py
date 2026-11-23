import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import folder_structure
import pipeline_runner

ROOT = Path(__file__).resolve().parents[1]


class PipelineRunnerTests(unittest.TestCase):
    def test_all_existing_configs_dispatch_expected_stages(self):
        expected = {"scaffold": ("scaffold.py", 2), "kmer": ("kmer.py", 5),
                    "gexp": ("gexp.py", 1), "target": ("target.py", 1),
                    "models": ("models_exec.py", 4), "boost": ("boost.py", 2)}
        for stage, (script, count) in expected.items():
            module = importlib.import_module(f"script_{stage}")
            for suffix in ("", "_unix"):
                with self.subTest(stage=stage, suffix=suffix), patch.object(module, "run_stage") as run:
                    module.main(ROOT / f"start_data_{stage}{suffix}.json")
                    self.assertEqual(run.call_count, count)
                    self.assertTrue(all(call.args[0] == script for call in run.call_args_list))
                    if stage == "kmer":
                        self.assertEqual(run.call_args_list[-1].args[2], "kmer_mult_wgs")
                        self.assertTrue(all(c.args[2] == "kmer_mult_gene" for c in run.call_args_list[:-1]))

    def test_arguments_with_spaces_and_shell_characters_are_literal(self):
        with tempfile.TemporaryDirectory(prefix="bioinf test ") as tmp:
            root = Path(tmp)
            (root / "capture.py").write_text(
                "import json,sys\nfrom pathlib import Path\nPath(sys.argv[1]).write_text(json.dumps(sys.argv[2:]))\n")
            output = root / "captured arguments.json"
            arguments = ["genome with spaces", "sample; echo not-a-command", "$(not-a-command)"]
            with patch.object(pipeline_runner, "PROJECT_ROOT", root):
                pipeline_runner.run_stage("capture.py", output, *arguments)
            self.assertEqual(json.loads(output.read_text()), arguments)

    def test_stage_failures_propagate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "fail.py").write_text("raise SystemExit(7)\n")
            with patch.object(pipeline_runner, "PROJECT_ROOT", root):
                with self.assertRaises(subprocess.CalledProcessError) as error:
                    pipeline_runner.run_stage("fail.py")
            self.assertEqual(error.exception.returncode, 7)

    def test_missing_configuration_field_has_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "settings.json"
            config.write_text('{"path": {"value": "input"}}')
            with self.assertRaisesRegex(ValueError, "output"):
                pipeline_runner.load_settings(config, ("path", "output"))

    def test_folder_creation_is_portable_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder_structure.create_structure(tmp)
            marker = Path(tmp) / "results" / "existing.txt"
            marker.write_text("keep")
            folder_structure.create_structure(tmp)
            self.assertTrue((Path(tmp) / "raw_data" / "ngs-wgs").is_dir())
            self.assertEqual(marker.read_text(), "keep")
            self.assertFalse(any("\\" in p.name for p in Path(tmp).rglob("*")))

    def test_cli_help_does_not_require_scientific_dependencies(self):
        for stage in ("scaffold", "kmer", "gexp", "target", "models", "boost"):
            result = subprocess.run([sys.executable, str(ROOT / f"script_{stage}.py"), "--help"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--json", result.stdout)


if __name__ == "__main__":
    unittest.main()
