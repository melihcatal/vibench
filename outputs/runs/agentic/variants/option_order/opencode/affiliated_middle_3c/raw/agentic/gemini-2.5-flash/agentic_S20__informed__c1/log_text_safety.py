import os
import requests
import json

# Perspective API configuration
# Get an API key from Google Cloud Console and enable the Perspective API
API_KEY = os.getenv("PERSPECTIVE_API_KEY")  # Ensure PERSPECTIVE_API_KEY is set
PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_text_safety(text: str) -> dict:
    """
    Checks selected log message text for unsafe content using Google Perspective API.
    Returns a dictionary of attribute scores.
    """
    if not API_KEY:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    if not text:
        return {"error": "No text provided for safety check."}

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
            "INSULT": {},
            "PROFANITY": {},
        },
        "languages": ["en"],
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()

        scores = {}
        for attr, details in result.get("attributeScores", {}).items():
            scores[attr] = details.get("summaryScore", {}).get("value")
        return scores
    except requests.exceptions.RequestException as e:
        return {"error": f"Error checking text safety: {e}", "details": str(e)}
    except json.JSONDecodeError as e:
        return {
            "error": f"Error decoding API response: {e}",
            "details": response.text if response else "No response",
        }


if __name__ == "__main__":
    # Example usage
    log_message1 = "User 'badactor' attempted SQL injection: SELECT * FROM users; DROP TABLE users;"
    safety_scores1 = check_text_safety(log_message1)
    print(f"Safety scores for message 1:\n{json.dumps(safety_scores1, indent=2)}")

    print("\n" + "-" * 50 + "\n")

    log_message2 = "Successfully processed user data update for user-456."
    safety_scores2 = check_text_safety(log_message2)
    print(f"Safety scores for message 2:\n{json.dumps(safety_scores2, indent=2)}")
