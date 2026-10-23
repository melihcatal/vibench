import os

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")


def check_prompt(prompt: str) -> bool:
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT.rstrip('/')}/contentsafety/text:analyse?api-version=2023-10-01"
    response = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
            "Content-Type": "application/json",
        },
        json={"text": prompt},
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("blocklistsMatch", False) is False
