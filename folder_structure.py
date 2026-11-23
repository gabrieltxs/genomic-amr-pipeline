"""Create the expected data/output folders without loading scientific libraries."""
from pathlib import Path

FOLDERS = (
    "lib/kmer", "lib/gexp", "lib/bond", "lib/boost", "lib/target", "lib/genes_eda_data",
    "raw_data/amr-phenotype", "raw_data/gexp-specialtygenes",
    "raw_data/ngs-specialtygenes", "raw_data/ngs-wgs", "scaffold", "results",
)


def create_structure(root):
    for folder in FOLDERS:
        (Path(root) / folder).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    create_structure(Path.cwd())
