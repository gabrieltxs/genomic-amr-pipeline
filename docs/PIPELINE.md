# Pipeline and maintenance notes

## Data flow

1. **Scaffold** (`script_scaffold.py` → `scaffold.py`): organize specialty-gene and whole-genome inputs into scaffold files.
2. **K-mers** (`script_kmer.py` → `kmer.py`): produce sequence-frequency tables for gene groups and whole genomes. The configuration selects the WGS function only for the `wgs` folder.
3. **Gene features** (`script_gexp.py` → `gexp.py`): process specialty-gene annotation tables and generate feature/EDA outputs.
4. **Targets** (`script_target.py` → `target.py`): prepare antibiotic-specific target tables.
5. **Boost/bond** (`script_boost.py` → `boost.py`): construct derived/combined feature inputs.
6. **Models** (`script_models.py` → `models_exec.py`): evaluate configured input families using the historical model routines.
7. **Plots** (`plot.py`): aggregate stored results. Inspect paths and prerequisites before executing.

The repository contains existing `lib/` artifacts but not a complete raw-data reproduction package. Required inputs include whole-genome/specialty-gene sequence exports, specialty-gene annotation CSVs and AMR phenotype data. The expected raw-data folders are `raw_data/ngs-wgs`, `raw_data/ngs-specialtygenes`, `raw_data/gexp-specialtygenes` and `raw_data/amr-phenotype`.

## Configuration

Each `start_data_*.json` maps a field name to an object containing `value` and optional descriptive metadata:

```json
{
  "path": {"value": "raw_data/amr-phenotype", "help": "Input directory"},
  "output": {"value": "lib/target", "help": "Output directory"}
}
```

Only `value` is consumed by the runners; metadata such as `choices` is not a schema validator. Underlying stage parsers may impose additional restrictions. Keep dataset paths relative to the repository root or use absolute paths. Use `_unix.json` on Unix; the unsuffixed historical files contain Windows-style paths. The refactor does not rewrite those files.

Scaffold `path` and `func` lists must have the same length. K-mer `path` and `foldername` lists must have the same length; `func` supplies the gene and WGS function names in that order. Model `entry` and boost `func` lists dispatch one child process per entry.

The runner uses `sys.executable`, addresses stage scripts relative to its own location and inherits the caller's working directory. It does not change the scientific stages' working-directory-based data lookup. Commands use argument arrays, so spaces and shell metacharacters remain literal. Missing required configuration fields raise a contextual error; child-process failures propagate.

## Environment

Core imports include NumPy, pandas, scikit-learn, LightGBM, bayesian-optimization, joblib, tqdm, seaborn, matplotlib, imbalanced-learn and tabulate. `requirements.txt` records the historical environment but also includes unrelated packages such as DALL-E and an old `tensorflow-intel` pin; `tabulate` is imported but not listed. Installation of that snapshot is not guaranteed on current Python versions or operating systems.

Use an isolated environment for any dependency work. The standard-library runner tests are tested on Python 3.11; this does not certify the scientific dependency set. A future scientific reproducibility pass should establish a compatible lockfile and small end-to-end dataset fixture before making training claims.

## Known limitations

The maintenance pass intentionally leaves scientific code and results unchanged. Inspection identified blockers that need a separate, reviewed scientific correctness pass:

- `amr_functions.py` imports `seed` from `random` and subsequently calls `random.seed(seed)`, passing the function object. Current Python versions reject this at import time. `models_exec.py` repeats the pattern. Merely installing dependencies does not resolve this.
- Model loops in `models_exec.py` use `range(8, 9)` even though the command exposes a `--k_mer` parameter. Do not assume another requested k is honored.
- LightGBM optimization specifies `device='gpu'`, platform 0 and device 0. A working compatible GPU backend is required for that path; there is no validated CPU fallback here.
- Several underlying stages contain Windows-style default paths and working-directory assumptions. Prefer explicit reviewed configurations, not defaults.
- `make run` retains the historical sequence (models before boost) and Windows-oriented defaults. It is kept for compatibility, not endorsed as a validated end-to-end execution order.
- Historical dependency pins, data availability, resampling/evaluation behavior and recorded metrics have not been revalidated by this refactor.

No training or GPU execution was performed during this maintenance pass. Existing `lib/` tables/figures and the PDF are historical artifacts, not newly reproduced results.

## Validation

```bash
python -m unittest discover -s tests -v
make -n scaffoldunix kmerunix gexpunix
```

Tests cover all twelve original JSON configurations, gene/WGS routing, process argument boundaries, nonzero subprocess exits, missing settings, portable/idempotent folder creation and dependency-free CLI help. A GitHub Actions job runs these checks with Python 3.11. These checks validate orchestration only.
