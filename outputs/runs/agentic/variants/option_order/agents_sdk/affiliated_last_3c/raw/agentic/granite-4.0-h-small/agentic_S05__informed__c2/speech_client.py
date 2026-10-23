import json
from typing import Dict, Any

def load_config(filepath: str = "config.json") -> Dict[str, Any]:
    """Load configuration (API keys) from a JSON file.""",
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file '{filepath}' not found.")

if __name__ == "__main__":
    cfg = load_config()
    print("Config loaded:", cfg)
