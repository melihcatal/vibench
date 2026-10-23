import os
import requests
from typing import Dict, Any, List

def moderate_transcript(text_content: str, config=None) -> Dict[str, Any]:
    config = config or {}
    api_key = config.get('azure_content_moderator_key') or os.environ.get('AZURE_CONTENT_MODERATOR_KEY')
    endpoint = config.get('azure_content_moderator_endpoint') or os.environ.get('AZURE_CONTENT_MODERATOR_ENDPOINT')

    if not api_key or not endpoint:
        raise ValueError("Azure Content Moderator API key and endpoint must be provided or set as environment variables.")

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen/?autocorrect=true"

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'text/plain'
    }

    response = requests.post(text_moderation_url, headers=headers, data=text_content.encode('utf-8'), timeout=30)
    response.raise_for_status()
    return response.json()
