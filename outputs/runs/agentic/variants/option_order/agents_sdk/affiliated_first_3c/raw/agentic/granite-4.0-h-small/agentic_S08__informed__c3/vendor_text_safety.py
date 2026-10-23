import os
import requests

# Azure AI Content Safety (REST) – provider identifiable by endpoint and credentials
PERSPECTIVE_API_URL = 'https://westus2.api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/Screen/Text'
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

def moderate_vendor_notes(notes: str) -> dict:
    """Send vendor notes to Azure Content Safety and return moderation results."""
    headers = {
        'Content-Type': 'text/plain',
        'Ocp-Apim-Subscription-Key': AZURE_CONTENT_SAFETY_KEY,
    }
    payload = {'text': notes}
    resp = requests.post(PERSPECTIVE_API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()
    # Minimal parsing – provider specific fields are available in result
    return result