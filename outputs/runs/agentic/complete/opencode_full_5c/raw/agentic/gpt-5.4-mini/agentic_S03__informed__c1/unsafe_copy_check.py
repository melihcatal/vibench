import os

import requests


def unsafe_copy_check(text: str) -> bool:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return bool(
        data.get("blocklistsMatch") or data.get("jailbreakAnalysis", {}).get("detected")
    )
