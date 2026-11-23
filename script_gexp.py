"""Run gexp.py from an existing start_data JSON configuration."""
import argparse
from pipeline_runner import load_settings, run_stage


def run_gexp(filename, list_genomes):
    run_stage("gexp.py", "-f", filename, "-l", list_genomes)


def main(json_file):
    data = load_settings(json_file, ('filename', 'list_genomes'))
    run_gexp(data["filename"], data["list_genomes"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-j", "--json", help="JSON configuration path", required=True)
    args = parser.parse_args()
    main(args.json)
