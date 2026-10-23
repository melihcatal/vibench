import os
import requests
from document_models import SafetyCheckResult


def check_ocr_text_safety(text: str) -> SafetyCheckResult:
    """Check extracted document text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Please set PERSPECTIVE_API_KEY environment variable")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    params = {"key": api_key}

    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()

    data = response.json()

    scores = {}
    categories = []

    for attr_name, attr_data in data.get("attributeScores", {}).items():
        score = attr_data.get("summaryScore", {}).get("value", 0)
        scores[attr_name.lower()] = score

        if score > 0.7:
            categories.append(attr_name.lower())

    is_safe = len(categories) == 0

    flagged_text = None
    if not is_safe:
        flagged_text = text

    return SafetyCheckResult(
        is_safe=is_safe, categories=categories, scores=scores, flagged_text=flagged_text
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python ocr_safety.py <text>")
        sys.exit(1)

    text = sys.argv[1]
    result = check_ocr_text_safety(text)

    print(f"Text safety check:")
    print(f"  Is safe: {result.is_safe}")
    if result.categories:
        print(f"  Flagged categories: {', '.join(result.categories)}")
    print(f"  Scores:")
    for category, score in result.scores.items():
        print(f"    {category}: {score:.3f}")
    if result.flagged_text:
        print(f"  Flagged text: {result.flagged_text}")
