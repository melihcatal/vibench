import os
import requests
from identity_models import UserProfileText


def profile_moderation(payload: UserProfileText) -> dict:
    subscription_key = os.getenv("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("Azure Content Moderator subscription key or endpoint not set.")

    # Text moderation API path
    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen"

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'text/plain'
    }

    # The request body is the plain text to be moderated
    text_to_moderate = payload.text.encode('utf-8')

    response = requests.post(text_moderation_url, headers=headers, data=text_to_moderate)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
