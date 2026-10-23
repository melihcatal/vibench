import os
import requests

def check_text_safety(text: str) -> dict:
    """
    Checks text for harmful content using the Google Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

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

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        scores = {
            attr: data["attributeScores"][attr]["summaryScore"]["value"]
            for attr in data["attributeScores"]
        }
        return scores
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
