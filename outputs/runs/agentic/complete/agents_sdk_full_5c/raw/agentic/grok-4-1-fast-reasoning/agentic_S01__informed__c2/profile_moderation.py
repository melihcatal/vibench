import os
import requests

def profile_moderation(profile_text: str, threshold: float = 0.7) -> bool:
    """
    Moderate profile text before account activation
    Returns True if safe
    """
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY required")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": profile_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {}
        },
        "languages": ["en"]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        toxicity = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        severe = data["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"]["value"]
        return toxicity < threshold and severe < 0.5
    except Exception:
        raise ValueError("Moderation failed")