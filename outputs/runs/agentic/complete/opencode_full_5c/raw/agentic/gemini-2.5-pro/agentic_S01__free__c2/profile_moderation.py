import os
import requests


def profile_moderation(text_content: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    payload = {
        "text": text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "breakByBlocklists": True,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()
