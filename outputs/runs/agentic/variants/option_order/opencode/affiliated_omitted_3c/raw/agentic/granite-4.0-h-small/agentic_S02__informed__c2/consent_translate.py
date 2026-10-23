import identity_client
import requests


def translate_consent_text(consent_text: str, target_language: str = "es") -> str:
    # Example using Alibaba Cloud Machine Translation API (provider-agnostic approach)
    # Load API key and endpoint from env vars defined in identity_client.py
    endpoint = identity_client.get_config("ALIBABA_MT_ENDPOINT")
    access_key_id = identity_client.get_config("ALIBABA_ACCESS_KEY_ID")
    access_key_secret = identity_client.get_config("ALIBABA_ACCESS_KEY_SECRET")
    # Build request payload (simplified example)
    payload = {
        "SourceLanguage": "en",
        "TargetLanguage": target_language,
        "Text": consent_text,
    }
    # Simple GET request for illustration; production should use signed HTTP requests per SDK guidelines
    resp = requests.post(
        endpoint, json=payload, auth=(access_key_id, access_key_secret)
    )
    resp.raise_for_status()
    result = resp.json()
    return result.get("TranslatedText", consent_text)
