"""Shared configuration and process execution for the historical stage CLIs."""
import json
from pathlib import Path
import shlex
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent


def load_settings(filename, required):
    """Read the existing JSON format, keeping metadata separate from values."""
    with Path(filename).open(encoding="utf-8") as stream:
        config = json.load(stream)
    try:
        return {key: config[key]["value"] for key in required}
    except (KeyError, TypeError) as error:
        raise ValueError(f"Configuration must define a value for: {', '.join(required)}") from error


def run_stage(script, *arguments):
    """Use this interpreter and preserve argument boundaries, without a shell."""
    command = [sys.executable, str(PROJECT_ROOT / script), *map(str, arguments)]
    print(f"Running command: {shlex.join(command)}", flush=True)
    subprocess.run(command, check=True)
    print(f"Command completed: {shlex.join(command)}", flush=True)
