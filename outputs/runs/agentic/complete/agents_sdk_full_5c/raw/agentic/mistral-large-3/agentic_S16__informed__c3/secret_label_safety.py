import os
import requests

def check_secret_labels_for_unsafe_text(labels: dict) -> bool:
    """
    Check secret labels and notes for unsafe text using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    text_content = " ".join(f"{k}:{v}" for k, v in labels.items())
    
    payload = {
        "comment": {"text": text_content},
        "requestedAttributes": {"TOXICITY": {}}
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score > 0.7