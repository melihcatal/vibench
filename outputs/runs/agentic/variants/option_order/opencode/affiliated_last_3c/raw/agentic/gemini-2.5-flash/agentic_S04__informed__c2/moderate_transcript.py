import os
import requests
import json


def moderate_text(text: str, endpoint: str, key: str) -> dict:
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {
        "text": text,
        "categories": {
            "Hate": True,
            "Sexual": True,
            "Violence": True,
            "SelfHarm": True,
        },
        "outputType": "FourSeverityLevels",
    }
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview",
        headers=headers,
        json=body,
    )
    response.raise_for_status()
    return response.json()
