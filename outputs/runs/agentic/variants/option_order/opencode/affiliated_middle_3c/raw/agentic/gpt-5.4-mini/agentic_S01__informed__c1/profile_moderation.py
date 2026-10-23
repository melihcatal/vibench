import os
import requests

from identity_models import normalize_text, response_payload


def profile_moderation(profile_text: str):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    r = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-10-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": normalize_text(profile_text)},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    return response_payload(
        {
            "provider": "Azure AI Content Safety",
            "result": data,
            "text": normalize_text(profile_text),
        }
    )
