import os
import requests


def check_platform_output_safety(text: str, endpoint: str, api_key: str):
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    json_data = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview",
        headers=headers,
        json=json_data,
    )
    response.raise_for_status()
    return response.json()
