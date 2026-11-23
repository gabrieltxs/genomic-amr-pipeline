# BIOINF

A research pipeline for **antimicrobial-resistance prediction** from genomic k-mer frequencies and specialty-gene annotations. The historical `Versão2-GPU` branch combines data preparation, feature extraction, feature boosting and LightGBM-based evaluation.

This is research code, not a clinical decision system. The command runners have lightweight automated tests; the historical scientific pipeline has **not** been revalidated on a complete dataset or GPU environment. See [known limitations](docs/PIPELINE.md#known-limitations) before running experiments.

## Repository map

| Location | Purpose |
| --- | --- |
| `script_*.py` | JSON-configured entry points for each stage |
| `pipeline_runner.py` | Shared JSON loading and subprocess execution |
| `scaffold.py`, `kmer.py`, `gexp.py`, `target.py`, `boost.py`, `models_exec.py` | Historical stage implementations |
| `amr_functions.py` | Shared scientific data processing, features and model evaluation |
| `start_data_*.json` | Original configuration files; `_unix` variants use Unix paths |
| `lib/` | Existing gene tables, target tables and exploratory artifacts |
| `docs/PIPELINE.md` | Data flow, configuration, environment and known limitations |
| `tests/` | Dependency-free checks of orchestration and directory setup |
| `BIOINF-Project-Pipeline.pdf` | Original pipeline diagram |

Root-level script names and JSON schemas are retained for compatibility with existing commands. Scientific implementations, parameters and tracked research artifacts are preserved.

## Quick start: inspect and test

The orchestration layer requires **Python 3.10+** and uses only the standard library:

```bash
git clone https://github.com/gabrieltxs/BIOINF.git
cd BIOINF
python -m unittest discover -s tests -v
python script_kmer.py --help
python folder_structure.py
```

Directory setup creates the expected folders without importing scientific dependencies or overwriting existing files. Tests do not train models, download datasets or require a GPU.

## Running research stages

Run commands from the repository root in a dedicated scientific environment. The original `requirements.txt` is a **legacy environment snapshot**, not a validated modern installation recipe. It includes unrelated and platform-specific packages and omits some imports; consult [environment notes](docs/PIPELINE.md#environment) before installing it.

1. Supply the raw genomic and phenotype data described in the pipeline guide.
2. Copy the relevant configuration file and update its `value` fields for your data paths and resources.
3. Execute one stage at a time and inspect its output before continuing.

For example, after preparing the required data and resolving the documented scientific-code blockers:

```bash
python script_scaffold.py -j start_data_scaffold_unix.json
python script_kmer.py -j start_data_kmer_unix.json
python script_gexp.py -j start_data_gexp_unix.json
python script_target.py -j start_data_target_unix.json
python script_boost.py -j start_data_boost_unix.json
python script_models.py -j start_data_models_unix.json
```

A nonzero stage exit now stops its runner instead of printing a misleading success message. Paths containing spaces are passed as single arguments. Existing Makefile stage names remain available (`make scaffoldunix`, `make kmerunix`, etc.). `make run` is a historical Windows-oriented sequence; it is not a validated one-command reproduction.

## Scope of this maintenance pass

- Consolidate duplicated configuration and process-launch code across six runners.
- Use the active Python interpreter and argument lists instead of shell commands.
- Correct the Unix scaffold, k-mer and gene-feature Makefile targets to select their own configurations.
- Create folders portably and without scientific imports or import-time side effects.
- Document actual entry points, prerequisites and unresolved scientific limitations.

No historical result, model setting, dataset or evaluation procedure is changed by this maintenance pass. Passing the runner checks does not establish scientific reproducibility or predictive performance.

## Author and licensing

Gabriel Sousa — [gabrieltxs](https://github.com/gabrieltxs).

The previous README claimed an MIT license, but this checkout has no `LICENSE` or `LICENSE.md` granting it. No license has been invented or added in this maintenance pass; contact the author to clarify reuse terms.
