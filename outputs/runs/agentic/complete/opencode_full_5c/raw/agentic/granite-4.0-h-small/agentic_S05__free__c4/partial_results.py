# [SAME-SCENARIO] partial_results.py
"""Helper utilities for handling partial and final streaming recognition results."""

from typing import Any, Dict, List, Optional


def extract_text(result: Dict[str, Any]) -> Optional[str]:
    """Return the transcript text for a single streaming result, or None if not available."""
    if not result.get("alternatives"):
        return None
    return result["alternatives"][0].get("transcript")


def merge_results(results: List[Dict[str, Any]]) -> str:
    """Concatenate transcripts from a list of results, preserving order."""
    return " ".join(extract_text(r) for r in results if extract_text(r))


if __name__ == "__main__":
    # Demo parsing a mock response payload
    mock_result = {
        "results": [
            {
                "alternatives": [{"transcript": "Hello"}],
                "is_final": False,
            },
            {
                "alternatives": [{"transcript": " world"}],
                "is_final": True,
            },
        ]
    }
    print(merge_results(mock_result["results"]))
