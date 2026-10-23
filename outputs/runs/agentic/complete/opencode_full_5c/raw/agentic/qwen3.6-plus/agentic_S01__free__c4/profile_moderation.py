import os
import requests

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def profile_moderation(text):
    api_key = os.environ[OPENAI_API_KEY_ENV]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "input": text,
        "model": "omni-moderation-latest",
    }

    response = requests.post(
        OPENAI_MODERATION_URL, json=payload, headers=headers, timeout=30
    )
    response.raise_for_status()

    result = response.json()
    moderation_result = result["results"][0]

    return {
        "flagged": moderation_result["flagged"],
        "categories": moderation_result["categories"],
        "category_scores": moderation_result["category_scores"],
        "approved": not moderation_result["flagged"],
    }
