"""Run models_exec.py from an existing start_data JSON configuration."""
import argparse
from pipeline_runner import load_settings, run_stage


def run_models(kmer, pathk, pathf, output, entry):
    run_stage("models_exec.py", "-k", kmer, "-pk", pathk, "-pf", pathf, "-o", output, "-e", entry)


def main(json_file):
    data = load_settings(json_file, ('kmer', 'pathk', 'pathf', 'output', 'entry'))
    for entry in data["entry"]:
        run_models(data["kmer"], data["pathk"], data["pathf"], data["output"], entry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-j", "--json", help="JSON configuration path", required=True)
    args = parser.parse_args()
    main(args.json)
