# embedding_job_summary.py
"""
[LATER-STEP] Summarize results of an embedding job (e.g., batch embedding or search).
"""

import json
from pathlib import Path


def summary_from_file(filepath: Path) -> str:
    """Read embedding JSON from file and return a concise textual summary.

    Args:
        filepath (Path): Path to the JSON file containing embedding results.

    Returns:
        str: Summary string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "embeddings" in data:
        summary = f"Found {len(data['embeddings'])} embeddings."
    else:
        summary = "No embeddings found in file."
    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python embedding_job_summary.py <path_to_json>")
        sys.exit(1)
    path = Path(sys.argv[1])
    print(summary_from_file(path))
