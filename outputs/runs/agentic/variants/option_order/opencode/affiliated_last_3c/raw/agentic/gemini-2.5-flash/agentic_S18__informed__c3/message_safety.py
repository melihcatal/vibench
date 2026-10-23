import os
import requests
from messaging_models import SafetyCheckResult

PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_content_safety(message_id: str, text_content: str) -> SafetyCheckResult:
    """
    Checks message payload text for unsafe content using the Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    attribute_scores = {}
    is_safe = True
    for attr, data in result.get("attributeScores", {}).items():
        score_value = data.get("summaryScore", {}).get("value", 0.0)
        attribute_scores[attr] = score_value
        # Define a threshold for "unsafe"
        if score_value > 0.7:  # Example threshold, adjust as needed
            is_safe = False

    return SafetyCheckResult(
        message_id=message_id, is_safe=is_safe, scores=attribute_scores
    )


if __name__ == "__main__":
    # Example usage:
    # export PERSPECTIVE_API_KEY="your-perspective-api-key"
    test_text_safe = "This is a perfectly safe message."
    test_text_unsafe = "You are an idiot and I hate you!"

    safety_result_safe = check_content_safety("msg-safe", test_text_safe)
    print(f"Safe Message Safety Check: {safety_result_safe}")

    safety_result_unsafe = check_content_safety("msg-unsafe", test_text_unsafe)
    print(f"Unsafe Message Safety Check: {safety_result_unsafe}")
