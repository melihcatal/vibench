import os
import requests
from typing import Dict, Any


def moderate_claims(text: str) -> Dict[str, Any]:
    # Using Azure Content Moderator
    endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_MODERATOR_KEY")
    
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "text/plain",
    }
    
    response = requests.post(
        f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen?autocorrect=False&PII=True&classify=True",
        headers=headers,
        data=text.encode("utf-8"),
    )
    response.raise_for_status()
    
    return response.json()