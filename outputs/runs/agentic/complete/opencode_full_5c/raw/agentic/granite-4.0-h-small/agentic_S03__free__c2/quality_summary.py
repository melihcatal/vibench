# quality_summary.py
import os
from typing import List, Dict
from translation_models import pretty_print

# Placeholder for a quality-assessment function that summarizes translation issues.
# In a real implementation this could call a language quality API or run checks on the translated text.


def summarize_quality(translation_results: List[str]) -> Dict[str, int]:
    """Dummy quality summary: counts length and flags empty translations."""
    summary = {
        "total": len(translation_results),
        "empty": sum(1 for t in translation_results if not t.strip()),
        "average_length": sum(len(t) for t in translation_results)
        / len(translation_results)
        if translation_results
        else 0,
    }
    return summary


if __name__ == "__main__":
    results = ["Hello world", "", "Bonjour"]
    print("Quality summary:", pretty_print([summarize_quality(results)]))
