import os
import requests


def check_platform_output_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    r = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
    )
    return r.json()
