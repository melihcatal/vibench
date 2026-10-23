import requests
import os

# Provider: OpenAI Moderation API
# Identifiable by: OPENAI_API_KEY, api.openai.com
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def message_safety(text: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"input": text}

    response = requests.post(OPENAI_MODERATION_URL, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return {
        "is_safe": not result["results"][0]["flagged"],
        "categories": result["results"][0]["categories"],
    }
