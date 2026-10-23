import os
import requests
import json


def check_corpus_safety(corpus_texts: list[str]) -> dict:
    """
    Checks corpus text for harmful content using the Azure AI Content Safety API.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    results = {}
    for i, text in enumerate(corpus_texts):
        payload = json.dumps({"text": text})
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        results[f"text_{i}"] = response.json()

    return results
