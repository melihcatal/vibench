import os
from googleapiclient import discovery
from typing import Dict, Any


def check_log_safety(log_text: str) -> Dict[str, Any]:
    """
    Checks log message text for unsafe content using the Perspective API.

    Note: The Perspective API is designed for user-generated content, but can be
    applied to log messages to find potentially sensitive or inappropriate text.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": log_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {}
        for attribute, data in response["attributeScores"].items():
            scores[attribute] = data["summaryScore"]["value"]
        return scores
    except Exception as e:
        print(f"Error calling Perspective API: {e}")
        return {}


if __name__ == "__main__":
    if not os.environ.get("PERSPECTIVE_API_KEY"):
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        # Example 1: A clean log message
        safe_log = "User successfully updated their profile information."
        safety_scores_safe = check_log_safety(safe_log)
        print(f"Safety scores for '{safe_log}':")
        print(safety_scores_safe)

        print("-" * 20)

        # Example 2: A log message containing potentially problematic text
        unsafe_log = "User 'idiot-user' left a horrible and threatening comment."
        safety_scores_unsafe = check_log_safety(unsafe_log)
        print(f"Safety scores for '{unsafe_log}':")
        print(safety_scores_unsafe)
