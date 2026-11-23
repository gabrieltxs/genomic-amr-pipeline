"""Run boost.py from an existing start_data JSON configuration."""
import argparse
from pipeline_runner import load_settings, run_stage


def boost(kmer, pathk, output, func):
    run_stage("boost.py", "-k", kmer, "-pk", pathk, "-o", output, "-f", func)


def main(json_file):
    data = load_settings(json_file, ('kmer', 'pathk', 'output', 'func'))
    for index, func in enumerate(data["func"], start=1):
        boost(data["kmer"], data["pathk"], data["output"], func)
        print(f"Progress: {index / len(data['func']) * 100:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-j", "--json", help="JSON configuration path", default="start_data_boost.json")
    args = parser.parse_args()
    main(args.json)
