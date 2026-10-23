from typing import Dict, Any
import requests

def check_text_safety(document: Dict[str, Any], field_name: str = "content") -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Google Cloud's Perspective API.
    """
    api_key = "<your-api-key>"
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    content = document.get(field_name, "")
    
    if not content:
        return {"safe": True, "scores": {}}

    payload = {
        "comment": {"text": content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {}
        }
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    
    return {
        "safe": all(score < 0.7 for score in result["attributeScores"].values()),
        "scores": result["attributeScores"]
    }