"""Run target.py from an existing start_data JSON configuration."""
import argparse
from pipeline_runner import load_settings, run_stage


def run_gexp(output, path):
    run_stage("target.py", "-o", output, "-p", path)


def main(json_file):
    data = load_settings(json_file, ('output', 'path'))
    run_gexp(data["output"], data["path"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-j", "--json", help="JSON configuration path", required=True)
    args = parser.parse_args()
    main(args.json)
