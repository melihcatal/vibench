import os
import requests


def check_prompt(prompt: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": prompt},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
