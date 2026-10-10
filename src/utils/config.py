"""Configuration loader: reads config/config.json and resolves paths."""
import json
from pathlib import Path

# Project root = two levels above src/utils/
ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = ROOT_DIR / "config" / "config.json"

DEFAULTS = {
    "data_file": "data/students.json",
    "log_file": "logs/app.log",
    "log_level": "INFO",
}


def load_config():
    """Load config, falling back to defaults if the file is missing/invalid."""
    config = dict(DEFAULTS)
    try:
        with open(CONFIG_FILE, "r") as f:
            config.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # use defaults

    # Make paths absolute so the app works from any working directory
    config["data_file"] = str(ROOT_DIR / config["data_file"])
    config["log_file"] = str(ROOT_DIR / config["log_file"])
    return config
