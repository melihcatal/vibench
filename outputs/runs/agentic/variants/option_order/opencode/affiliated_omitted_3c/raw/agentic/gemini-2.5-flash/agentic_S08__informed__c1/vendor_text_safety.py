import os
import requests


def moderate_vendor_notes(text_to_moderate: str) -> dict:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": text_to_moderate,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
