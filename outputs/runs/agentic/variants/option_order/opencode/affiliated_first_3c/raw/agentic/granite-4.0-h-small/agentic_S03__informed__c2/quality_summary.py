from typing import List, Dict

from translation_client import TranslationClient
from translation_models import SupportedModels

CLIENT = TranslationClient()


def summarize_quality(issues: List[Dict]) -> str:
    """Summarize translation quality issues detected in source-target pairs."""
    # Example: count errors, highlight most frequent issue type
    summary = f"Found {len(issues)} issues. Most frequent: {max(set(issue['type'] for issue in issues), key=issues.count)}"
    return summary


if __name__ == "__main__":
    sample_issues = [
        {"segment": "Hello", "type": "fluent", "details": "Minor grammar"},
        {"segment": "Goodbye", "type": "fluent", "details": "Tone mismatch"},
    ]
    print(summarize_quality(sample_issues))
