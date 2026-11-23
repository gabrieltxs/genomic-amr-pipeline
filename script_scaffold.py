"""Run scaffold.py from an existing start_data JSON configuration."""
import argparse
from pipeline_runner import load_settings, run_stage


def run_scaffold(main, file_path, output_path):
    run_stage("scaffold.py", "-f", main, "-p", file_path, "-o", output_path)


def main(json_file):
    data = load_settings(json_file, ('path', 'func', 'output'))
    for index, (func, path) in enumerate(zip(data["func"], data["path"], strict=True), start=1):
        run_scaffold(func, path, data["output"])
        print(f"Progress: {index / len(data['path']) * 100:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-j", "--json", help="JSON configuration path", default=None)
    args = parser.parse_args()
    if args.json:
        main(args.json)
    else:
        parser.print_help()
