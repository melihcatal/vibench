from typing import Dict, Any
import requests

def check_platform_output_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
        },
        "languages": ["en"],
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return {
        "safe": response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.7,
        "scores": response.json()["attributeScores"],
    }