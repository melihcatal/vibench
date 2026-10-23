import os
import requests

def score_image_safety(image_bytes: bytes) -> dict:
    """
    Checks an image for unsafe or policy-sensitive visual content using Azure Content Moderator.
    """
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("Azure Content Moderator subscription key or endpoint not found in environment variables.")

    image_moderation_url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessImage/Evaluate"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }

    response = requests.post(image_moderation_url, headers=headers, data=image_bytes)
    response.raise_for_status()
    return response.json()
