import os
import requests
import uuid
from typing import Dict, Any, List


def translate_record_field(text_to_translate: str, target_language: str = "es") -> str:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables not set."
        )

    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text_to_translate}]

    params = {"api-version": "3.0", "to": target_language}

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    request.raise_for_status()

    if (
        response
        and isinstance(response, list)
        and "translations" in response[0]
        and response[0]["translations"]
    ):
        return response[0]["translations"][0]["text"]
    return text_to_translate
