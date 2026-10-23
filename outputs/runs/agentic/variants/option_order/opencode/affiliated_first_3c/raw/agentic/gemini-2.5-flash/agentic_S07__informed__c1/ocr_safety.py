import os
import requests
from document_models import TextExtractionResult, SafetyCheckResult


def check_safety(
    text_to_check: TextExtractionResult, api_key: str
) -> SafetyCheckResult:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    data = {
        "comment": {"text": text_to_check.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    result = response.json()

    attribute_scores = {}
    for attribute, scores in result.get("attributeScores", {}).items():
        attribute_scores[attribute] = scores["summaryScore"]["value"]

    return SafetyCheckResult(attribute_scores=attribute_scores)


if __name__ == "main":
    PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")

    if not PERSPECTIVE_API_KEY:
        print("Please set PERSPECTIVE_API_KEY environment variable.")
    else:
        sample_text = TextExtractionResult(text="You are an idiot.")
        safety_result = check_safety(sample_text, PERSPECTIVE_API_KEY)
        print(f"Text: {sample_text.text}")
        print("Safety Check Results:", safety_result.attribute_scores)
