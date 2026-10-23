import requests
import os

# Perspective API configuration
# Ensure PERSPECTIVE_API_KEY environment variable is set
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_profile_text(text: str, client_ip: str = "127.0.0.1") -> dict:
    """
    Moderates profile text before account activation using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}"

    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "doNotStore": True,
        "clientToken": client_ip # Optional: for rate limiting/abuse detection
    }

    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status()
        analysis_result = response.json()

        # Extract scores
        attribute_scores = {}
        for attribute, data in analysis_result.get("attributeScores", {}).items():
            attribute_scores[attribute] = data.get("summaryScore", {}).get("value")

        return {
            "text": text,
            "scores": attribute_scores,
            "message": "Profile text moderated successfully."
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        return {"error": error_data.get("error", {}).get("message", str(e))}
    except Exception as e:
        return {"error": str(e)}
