import requests
import os


def message_safety(payload_text: str) -> Dict[str, Any]:
    """
    Checks message payload text for unsafe content using Perspective API.

    Args:
        payload_text: The text payload to check for safety.

    Returns:
        Dict[str, Any]: Safety analysis results including toxicity scores.
    """
    # Load Perspective API key from environment variables
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Prepare request data
    data = {
        "comment": {"text": payload_text},
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

    # Call Perspective API
    response = requests.post(url, json=data)
    response.raise_for_status()

    result = response.json()

    return {
        "payload_text": payload_text,
        "safety_scores": result.get("attributeScores", {}),
    }
