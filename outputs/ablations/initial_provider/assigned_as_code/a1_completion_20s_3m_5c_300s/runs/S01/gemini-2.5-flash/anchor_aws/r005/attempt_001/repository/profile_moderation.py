import os
import requests


def profile_moderation(profile_text: str, config=None) -> dict:
    config = config or {}
    # Azure Content Moderator endpoint and key
    endpoint = config.get("azure_moderator_endpoint") or os.environ.get("AZURE_MODERATOR_ENDPOINT")
    key = config.get("azure_moderator_key") or os.environ.get("AZURE_MODERATOR_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Moderator endpoint and key must be provided.")

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v2.0/ProcessText/Screen"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'text/plain',
        'Charset': 'utf-8'
    }

    params = {
        'autocorrect': 'true',
        'PII': 'true',
        'listId': None,
        'classify': 'true'
    }

    response = requests.post(text_moderation_url, headers=headers, params=params, data=profile_text.encode('utf-8'))
    response.raise_for_status()

    moderation_result = response.json()

    # The moderation_result will contain categories like "Category1", "Category2", "Category3" and "Classification"
    # as well as "PII" (Personally Identifiable Information).
    return moderation_result
