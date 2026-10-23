from typing import Dict, Any
import requests
from messaging_models import EventResponse

PERSPECTIVE_API_KEY = "AIza..."
PERSPECTIVE_API_URL = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"

def check_message_safety(message: EventResponse) -> bool:
    text = str(message.payload.get("text", ""))
    if not text:
        return True
    
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    response = requests.post(PERSPECTIVE_API_URL, json=payload)
    response.raise_for_status()
    
    toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score < 0.7