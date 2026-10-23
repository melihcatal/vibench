import os
from typing import List
from translation_models import TranslationScore, QualityIssue, QualityIssueType

# Placeholder for actual unsafe content detection logic
# Example implementation uses provider-specific "unsafe_content" flag


def check_unsafe_content(
    translated_texts: List[str], scores: List[TranslationScore]
) -> List[str]:
    """Check localized copy for unsafe content.

    Args:
        translated_texts: List of translated strings.
        scores: Parallel list of TranslationScore objects with quality issue data.

    Returns:
        List of strings describing unsafe content issues, empty list if none.
    """
    unsafe = []
    for score in scores:
        if (
            score.get("quality_issue")
            and score["quality_issue"]["type"] == "unsafe_content"
        ):
            unsafe.append(score["quality_issue"]["description"])
    return unsafe


# Example usage with simulated scores
# if __name__ == "__main__":
#     example_translations = ["This is safe.", "This is unsafe: hate speech."]
#     example_scores = [
#         {"quality_issue": None, "raw_score": 95, "normalized_score": 0.95},
#         {"quality_issue": {"type": "unsafe_content", "description": "Hate speech detected", "severity": "error"}, "raw_score": 40, "normalized_score": 0.4}
#     ]
#     print(check_unsafe_content(example_translations, example_scores))
