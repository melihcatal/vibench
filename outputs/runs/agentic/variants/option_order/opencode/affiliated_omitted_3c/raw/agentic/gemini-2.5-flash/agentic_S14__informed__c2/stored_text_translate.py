import os
import requests
import uuid


def translate_text(text: str, target_language: str = "en") -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = os.getenv(
        "AZURE_TRANSLATOR_ENDPOINT"
    )  # This would be like https://api.cognitive.microsofttranslator.com/
    location = os.getenv(
        "AZURE_TRANSLATOR_REGION"
    )  # This is the region, e.g., "global" or "westus2"

    if not key or not endpoint or not location:
        raise ValueError(
            "AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_ENDPOINT, and AZURE_TRANSLATOR_REGION environment variables must be set."
        )

    path = "/translate"
    constructed_url = endpoint + path

    params = {"api-version": "3.0", "to": target_language}

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if response and isinstance(response, list) and response[0].get("translations"):
        return response[0]["translations"][0]["text"]
    else:
        return f"Translation failed or returned unexpected format: {response}"
