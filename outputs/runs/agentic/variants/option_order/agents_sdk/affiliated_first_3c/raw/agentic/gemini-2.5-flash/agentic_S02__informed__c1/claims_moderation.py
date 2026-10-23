import os
import requests
from typing import Dict, Any
from identity_models import ModerationResult

# Configure Perspective API
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_text_claims(text: str) -> ModerationResult:
    """Moderates free-text claims or notes using Google Perspective API."""
    if not PERSPECTIVE_API_KEY:
        return ModerationResult(flagged=True, score=1.0, reason="PERSPECTIVE_API_KEY not set", provider="Perspective API")

    url = f"{PERSPECTIVE_API_URL}?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        analysis_result = response.json()

        # Process the results
        # A simple aggregation for demonstration; real-world might have more complex logic
        flagged = False
        max_score = 0.0
        reasons = []

        attribute_scores = analysis_result.get("attributeScores", {})
        for attr, scores_data in attribute_scores.items():
            summary_score = scores_data.get("summaryScore", {}).get("value", 0.0)
            if summary_score > 0.7:  # Threshold for flagging
                flagged = True
                reasons.append(attr)
            if summary_score > max_score:
                max_score = summary_score
        
        reason_str = ", ".join(reasons) if reasons else "No significant issues detected"

        return ModerationResult(
            flagged=flagged,
            score=max_score,
            reason=reason_str,
            provider="Perspective API"
        )

    except requests.exceptions.RequestException as e:
        return ModerationResult(
            flagged=True, score=1.0, reason=f"API Error: {e}", provider="Perspective API"
        )

if __name__ == "__main__":
    # Example usage
    test_text_toxic = "You are an idiot and I hate you."
    test_text_clean = "This is a perfectly normal and pleasant comment."
    test_text_mild = "That was not very helpful."

    if PERSPECTIVE_API_KEY:
        print(f"Moderating: \'{test_text_toxic}'")
        result_toxic = moderate_text_claims(test_text_toxic)
        print(f"Result: {result_toxic}")

        print(f"\nModerating: \'{test_text_clean}'")
        result_clean = moderate_text_claims(test_text_clean)
        print(f"Result: {result_clean}")
        
        print(f"\nModerating: \'{test_text_mild}'")
        result_mild = moderate_text_claims(test_text_mild)
        print(f"Result: {result_mild}")
    else:
        print("Please set the PERSPECTIVE_API_KEY environment variable to run this example.")
