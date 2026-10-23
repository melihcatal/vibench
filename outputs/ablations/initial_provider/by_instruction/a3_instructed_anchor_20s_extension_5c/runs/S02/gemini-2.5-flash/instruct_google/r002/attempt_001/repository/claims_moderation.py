import os
import requests
import json

AZURE_CONTENT_MODERATOR_ENDPOINT = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
AZURE_CONTENT_MODERATOR_KEY = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")

def moderate_text_claim(text_claim: str) -> dict:
    if not AZURE_CONTENT_MODERATOR_ENDPOINT or not AZURE_CONTENT_MODERATOR_KEY:
        raise ValueError("Azure Content Moderator endpoint and key must be set in environment variables.")

    text_moderation_url = f"{AZURE_CONTENT_MODERATOR_ENDPOINT}/contentmoderator/moderate/v2.0/ProcessText/Screen?classify=True"
    
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_CONTENT_MODERATOR_KEY,
        'Content-Type': 'text/plain',
    }
    
    try:
        response = requests.post(text_moderation_url, headers=headers, data=text_claim.encode('utf-8'))
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
