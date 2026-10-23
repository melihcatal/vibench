import os
import requests
import json
from typing import Dict, Any

# NOTE: This assumes Azure Content Moderator is configured with an API key and endpoint.

def check_unsafe_content(text_to_check: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    moderator_key = config.get("azure_content_moderator_api_key") or os.environ.get("AZURE_CONTENT_MODERATOR_API_KEY")
    moderator_endpoint = config.get("azure_content_moderator_endpoint") or os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not moderator_key or not moderator_endpoint:
        raise ValueError("Azure Content Moderator API key and endpoint must be provided or set as environment variables.")

    text_moderation_url = f"{moderator_endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen?classify=True"

    headers = {
        'Ocp-Apim-Subscription-Key': moderator_key,
        'Content-Type': 'text/plain'
    }

    response = requests.post(text_moderation_url, headers=headers, data=text_to_check.encode('utf-8'))
    response.raise_for_status()
    
    result = response.json()
    
    # Simplified output for demonstration; full response contains more details
    classification = result.get('Classification', {})
    is_unsafe = classification.get('ReviewRecommended', False)

    return {
        "text": text_to_check,
        "is_unsafe": is_unsafe,
        "classification_details": classification # Provides details like Category1, Category2, Category3
    }
