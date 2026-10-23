import os
import requests
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Azure AI Content Safety as the content moderation provider
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

CONTENT_SAFETY_URI = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text/v1.0"

HEADERS = {
    "api-key": AZURE_CONTENT_SAFETY_KEY,
    "Content-Type": "application/json",
}

def moderate_profile_text(text: str, locale: str = 'en') -> str:
    """Moderate profile text before account activation.

    Sends the supplied text to Azure Content Safety for profanity and hateful content detection.
    If the content is flagged, a sanitized version is returned (simple placeholder implementation).
    Raises IdentityError for service failures.
    """
    payload = {
        "contentType": "text/plain",
        "content": text,
        "modelId": "default",  # use default model; replace with specific model if needed
        "locale": locale,
    }
    response = requests.post(CONTENT_SAFETY_URI, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise IdentityError(f"Content moderation request failed: {response.text}")
    result = response.json()
    # Simplified: if any flags are present, return a sanitized placeholder
    if result.get('result') == 'BLOCKED':
        return "[MODERATION: CONTENT BLOCKED]\n"
    return text
