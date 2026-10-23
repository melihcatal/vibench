import os
import requests
import json


def check_content_safety(text: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    data = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "breakByBlocklists": False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()
