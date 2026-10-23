import os
import requests
import json
from typing import List

def moderate_transcript(text: str) -> dict:
    subscription_key = os.environ.get("CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    endpoint = os.environ.get("CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("Content Moderator subscription key and endpoint must be set in environment variables.")

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v2.0/ProcessText/Screen?classify=True"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "text/plain"
    }

    response = requests.post(text_moderation_url, headers=headers, data=text.encode('utf-8'))
    response.raise_for_status()

    return response.json()
