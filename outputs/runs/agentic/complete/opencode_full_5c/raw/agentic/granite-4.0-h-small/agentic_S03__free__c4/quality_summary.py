# quality_summary.py
from typing import List, Dict
from translation_models import TranslateResponse


def summarize_quality(
    translation_results: List[TranslateResponse], original_texts: List[str]
) -> Dict[str, int]:
    """Analyze translated texts and summarize common quality issues compared to originals."""
    issues = {"word_order": 0, "missing_terms": 0, "excessive_length": 0}
    for orig, trans in zip(original_texts, translation_results):
        # Simple heuristic checks
        if len(trans["translated_text"]) > 1.5 * len(orig):
            issues["excessive_length"] += 1
        if any(word not in trans["translated_text"] for word in orig.split()[:3]):
            issues["missing_terms"] += 1
        if not all(
            char.isascii() or char.isspace() for char in trans["translated_text"]
        ):
            issues["word_order"] += 1  # placeholder for complex reorder detection
    return issues
