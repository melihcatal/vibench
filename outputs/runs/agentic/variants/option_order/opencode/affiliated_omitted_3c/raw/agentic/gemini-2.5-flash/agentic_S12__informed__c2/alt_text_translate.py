import os
import requests
import uuid


def translate_alt_text(text: str, target_language: str = "es") -> str:
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    endpoint = os.environ.get(
        "AZURE_TRANSLATOR_ENDPOINT"
    )  # Note: The prompt mentioned AZURE_TRANSLATOR_REGION, but Azure Translator typically uses an endpoint URL.
    location = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not key or not endpoint or not location:
        raise ValueError(
            "AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_ENDPOINT, and AZURE_TRANSLATOR_REGION environment variables must be set."
        )

    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    params = {"api-version": "3.0", "to": target_language}

    body = [{"text": text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if response and isinstance(response, list) and "translations" in response[0]:
        return response[0]["translations"][0]["text"]
    return text  # Return original text if translation fails
