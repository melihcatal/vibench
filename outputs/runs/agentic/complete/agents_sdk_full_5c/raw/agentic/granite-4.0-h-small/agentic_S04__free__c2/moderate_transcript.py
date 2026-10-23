import os
import requests
from typing import Any, Dict

# Assume Azure Content Safety (or Azure AI Content Safety) for transcript moderation
MODERATION_ENDPOINT = "https://<your-resource-name>.cognitiveservices.azure.com"
MODERATION_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

#
# Moderate transcript text before publishing
def moderate_transcript(transcript: str) -> Dict[str, Any]:
    """Send transcript text to Azure Content Safety and return the moderation result.",
    The service returns a JSON with a 'label' (e.g., 'Safe' / 'Unsafe') and confidence scores.",
    """
    path = "/contentmoderator/moderate/text/"
    url = f"{MODERATION_ENDPOINT}{path}"
    headers = {
        "Ocp-Apim-Subscription-Key": MODERATION_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "content": transcript,
        "model": {"type": "default"},
        "listId": None,  # optional custom blocklist
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    # Simplify to just label and score for downstream steps
    return {
        "label": result.get("labels", [{}])[0].get("name"),
        "score": result.get("scores", {}),
    }

# Export only the moderation helper
__all__ = ["moderate_transcript"]
