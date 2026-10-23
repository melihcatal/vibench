import os
from translation_models import TranslationScore, QualityIssue


def summarize_quality(scores: list[TranslationScore]) -> str:
    """Summarize translation quality issues across a batch.

    Args:
        scores: List of TranslationScore objects from provider.

    Returns:
        Human-readable summary string.
    """
    issue_counts = {"unsafe_content": 0, "fluent": 0, "consistent": 0}
    for s in scores:
        if s.get("quality_issue"):
            issue_type = s["quality_issue"]["type"]
            issue_counts[issue_type] += 1
    summary = "Quality Summary:\\n"
    for issue, count in issue_counts.items():
        summary += f"  {issue.replace('_', ' ').title()}: {count}\\n"
    return summary


# Example usage (when scoring functions are implemented elsewhere)
# if __name__ == "__main__":
#     # simulated batch scores
#     batch_scores = [
#         {"quality_issue": {"type": "unsafe_content", "description": "Adult content detected", "severity": "error"}, "raw_score": 78, "normalized_score": 0.8},
#         {"quality_issue": None, "raw_score": 92, "normalized_score": 0.95},
#         {"quality_issue": {"type": "fluent", "description": "Minor fluency issue", "severity": "warning"}, "raw_score": 85, "normalized_score": 0.9},
#     ]
#     print(summarize_quality(batch_scores))
