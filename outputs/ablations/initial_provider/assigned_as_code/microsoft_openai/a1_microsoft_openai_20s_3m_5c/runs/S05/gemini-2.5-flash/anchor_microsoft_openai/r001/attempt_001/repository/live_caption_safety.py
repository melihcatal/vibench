import os
import requests
import json

def check_caption_safety(text: str):
    """
    Checks live transcript text for unsafe content using Azure Content Moderator.
    Returns a dictionary with moderation results.
    """
    key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not key or not endpoint:
        raise ValueError("AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables must be set.")

    # Text moderation path
    text_moderation_path = '/contentmoderator/moderate/v1.0/ProcessText/Screen?classify=True'
    constructed_url = endpoint + text_moderation_path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-type': 'text/plain',
        'Accept': 'application/json'
    }

    # The body is the plain text to moderate
    body = text

    request = requests.post(constructed_url, headers=headers, data=body.encode('utf-8'))
    response_json = request.json()

    if request.status_code != 200:
        raise RuntimeError(f"Azure Content Moderator API error: {response_json}")

    return response_json
