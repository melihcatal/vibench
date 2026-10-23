import os
from typing import Dict
import requests

# Azure AI Content Safety
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

def moderate_claims(claims: Dict) -> bool:
    text_claims = " ".join([str(v) for v in claims.values() if isinstance(v, str)])
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text_claims,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    return all(block["severity"] < 2 for block in result["categoriesAnalysis"])