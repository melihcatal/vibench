import os
import requests


def record_text_safety(text_content: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    api_version = "2023-10-15-preview"

    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {
        "text": text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()
