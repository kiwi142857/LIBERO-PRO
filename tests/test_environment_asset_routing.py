import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import perturbation


class OutputSuiteNameTests(unittest.TestCase):
    def test_no_perturbation_keeps_generated_assets_out_of_source_suite(self):
        result = perturbation.resolve_output_suite_name(
            "libero_spatial", perturbation.PerturbFlags(), {}
        )

        self.assertEqual(result, "libero_spatial_temp")

    def test_single_environment_perturbation_uses_env_suite(self):
        flags = perturbation.PerturbFlags(use_environment=True)

        result = perturbation.resolve_output_suite_name(
            "libero_spatial", flags, {"use_environment": "env"}
        )

        self.assertEqual(result, "libero_spatial_env")

    def test_combined_perturbations_use_temp_suite(self):
        flags = perturbation.PerturbFlags(
            use_environment=True,
            use_language=True,
        )

        result = perturbation.resolve_output_suite_name(
            "libero_spatial",
            flags,
            {"use_environment": "env", "use_language": "lan"},
        )

        self.assertEqual(result, "libero_spatial_temp")

    def test_single_perturbation_requires_a_folder_mapping(self):
        flags = perturbation.PerturbFlags(use_environment=True)

        with self.assertRaisesRegex(ValueError, "use_environment"):
            perturbation.resolve_output_suite_name("libero_spatial", flags, {})


class CreateEnvironmentTests(unittest.TestCase):
    def test_process_bddl_keeps_positional_seed_compatibility(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "libero_spatial"
            source_dir.mkdir()
            (source_dir / "task.bddl").write_text(
                "(define (problem LIBERO_Tabletop_Manipulation))",
                encoding="utf-8",
            )

            output_dir = perturbation.process_bddl_file_mixed(
                str(source_dir),
                "libero_spatial",
                perturbation.PerturbFlags(),
                {},
                42,
            )

            self.assertEqual(output_dir, f"{source_dir}_temp")

    def test_environment_assets_are_generated_in_the_env_suite(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "bddl_files" / "libero_spatial"
            source_dir.mkdir(parents=True)
            (source_dir / "task.bddl").write_text(
                "(define (problem LIBERO_Tabletop_Manipulation))",
                encoding="utf-8",
            )
            init_root = root / "init_files"

            config = {
                "bddl_files_path": str(source_dir),
                "task_suite_name": "libero_spatial",
                "init_file_dir": str(init_root),
                "script_path": "generate_init_states.py",
                "use_environment": True,
                "use_swap": False,
                "use_object": False,
                "use_language": False,
                "use_task": False,
                "ood_task_configs": {},
                "perturbation_mapping": {"use_environment": "env"},
            }

            with patch.object(perturbation, "EvalEnvCreator") as creator_cls:
                output_suite = perturbation.create_env(configs=config)

            output_bddl = root / "bddl_files" / "libero_spatial_env" / "task.bddl"
            self.assertEqual(output_suite, "libero_spatial_env")
            self.assertTrue(output_bddl.exists())
            creator_cls.assert_called_once_with(
                input_dir=str(root / "bddl_files" / "libero_spatial_env"),
                script_path="generate_init_states.py",
                base_output_dir=str(init_root),
            )
            creator_cls.return_value.create_env.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
