import os
import requests


def ocr_translate(text: str, target_language: str = "es") -> str:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION must be set in environment variables"
        )

    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(java.util.UUID.randomUUID())
        if "java.util.UUID" in globals()
        else "",  # Placeholder for UUID, if it existed in Python
    }

    params = {"api-version": "3.0", "to": target_language}

    body = [{"text": text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if response and isinstance(response, list) and "translations" in response[0]:
        return response[0]["translations"][0]["text"]
    return ""
