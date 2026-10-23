import os
import requests

def check_text_safety(text: str) -> dict:
    """
    Checks generated visual labels for unsafe text using Azure Text Analytics.
    """
    text_analytics_key = os.environ.get("AZURE_TEXT_ANALYTICS_SUBSCRIPTION_KEY")
    text_analytics_endpoint = os.environ.get("AZURE_TEXT_ANALYTICS_ENDPOINT")

    if not text_analytics_key or not text_analytics_endpoint:
        raise ValueError("Azure Text Analytics subscription key or endpoint not found in environment variables.")

    # Using Content Moderator's text API for consistency with image moderation
    text_moderation_url = f"{text_analytics_endpoint}/contentmoderator/moderate/v1.0/ProcessText/FullText"
    headers = {
        'Ocp-Apim-Subscription-Key': text_analytics_key,
        'Content-Type': 'text/plain'
    }

    response = requests.post(text_moderation_url, headers=headers, data=text.encode('utf-8'))
    response.raise_for_status()
    return response.json()
