# retrieval_audio_brief.py
"""
[LATER-STEP] Generate a spoken brief from retrieved search results.
"""

import json
from pathlib import Path


def create_audio_brief(results_file: Path) -> str:
    """Create a concise spoken text brief from JSON search results.

    Assumes the JSON contains a list of documents with a 'title' field.

    Args:
        results_file (Path): Path to the JSON file with search results.

    Returns:
        str: Text that can be fed to a TTS engine.
    """
    with open(results_file, "r", encoding="utf-8") as f:
        results = json.load(f)
    # Extract titles (max 5) for brief
    titles = [item.get("title", "Untitled") for item in results[:5]]
    brief = "Here are the top results: "
    brief += ", ".join(f"{i + 1}: {title}" for i, title in enumerate(titles))
    return brief


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python retrieval_audio_brief.py <results_json_file>")
        sys.exit(1)
    path = Path(sys.argv[1])
    brief = create_audio_brief(path)
    print("Audio brief:", brief)
