import os

import requests


def metric_annotation_safety(text: str):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    response = requests.post(
        url,
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
