"""Run kmer.py from an existing start_data JSON configuration."""
import argparse
from pipeline_runner import load_settings, run_stage


def run_kmer_extraction(main, file_path, output_path, k_value, foldername, core_num):
    run_stage("kmer.py", "-f", main, "-k", k_value, "-p", file_path, "-o", output_path, "-fn", foldername, "-c", core_num)


def main(json_file):
    data = load_settings(json_file, ('path', 'foldername', 'func', 'output', 'k_mer', 'cores'))
    for index, (path, folder) in enumerate(zip(data["path"], data["foldername"], strict=True), start=1):
        func = data["func"][1 if folder == "wgs" else 0]
        run_kmer_extraction(func, path, data["output"], data["k_mer"], folder, int(data["cores"]))
        print(f"Progress: {index / len(data['path']) * 100:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-j", "--json", help="JSON configuration path", default=None)
    args = parser.parse_args()
    if args.json:
        main(args.json)
    else:
        parser.print_help()
