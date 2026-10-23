import os
import requests
import uuid
import json


def translate_consent_copy(
    text: str, target_language: str = "es", source_language: str = "en"
) -> str:
    # Azure Translator endpoint and subscription key are identifiable signals
    key = os.environ.get("AZURE_TRANSLATOR_KEY", "your_azure_translator_key")
    endpoint = os.environ.get(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    )
    location = os.environ.get("AZURE_TRANSLATOR_LOCATION", "global")  # e.g., "westus2"

    if (
        key == "your_azure_translator_key"
        or endpoint == "https://api.cognitive.microsofttranslator.com"
    ):
        print(
            "Please configure AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_ENDPOINT environment variables."
        )
        return f"Translation service not configured for: '{{text}}'"

    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    params = {"api-version": "3.0", "from": source_language, "to": [target_language]}

    body = [{"text": text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = text
    if response and isinstance(response, list) and "translations" in response[0]:
        translated_text = response[0]["translations"][0]["text"]
        print(f"Original: '{{text}}'")
        print(f"Translated ({{target_language}}): '{{translated_text}}'")
    else:
        print(
            f"Error or unexpected response from Azure Translator: {json.dumps(response, indent=2)}"
        )

    return translated_text


if __name__ == "__main__":
    # Example usage
    consent_text = (
        "By clicking 'Accept', you agree to our terms of service and privacy policy."
    )
    translate_consent_copy(consent_text, target_language="fr")
    translate_consent_copy(consent_text, target_language="de")
