import os
import requests
from typing import Dict, Any


def moderate_vendor_text_safety(text_to_moderate: str, config=None) -> Dict[str, Any]:
    config = config or {}
    endpoint = config.get('AZURE_CONTENT_MODERATOR_ENDPOINT', os.environ.get('AZURE_CONTENT_MODERATOR_ENDPOINT'))
    subscription_key = config.get('AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY', os.environ.get('AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY'))

    if not endpoint or not subscription_key:
        raise ValueError("Azure Content Moderator endpoint and subscription key must be provided in config or environment variables.")

    url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen?classify=True"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'text/plain',
    }

    try:
        response = requests.post(url, headers=headers, data=text_to_moderate)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"Azure Content Moderator API error: {e}"}
