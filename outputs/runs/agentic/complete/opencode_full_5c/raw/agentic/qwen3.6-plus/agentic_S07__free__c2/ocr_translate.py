import requests
from document_client import AZURE_TRANSLATOR_ENDPOINT, get_azure_translator_headers


AZURE_TRANSLATOR_API_URL = "https://api.cognitive.microsofttranslator.com/translate"


def translate_text(
    text: str, target_language: str = "en", source_language: str = None
) -> dict:
    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    body = [{"text": text}]
    headers = get_azure_translator_headers()

    response = requests.post(
        AZURE_TRANSLATOR_API_URL, params=params, headers=headers, json=body
    )
    response.raise_for_status()
    result = response.json()
    return result[0]


def translate_ocr_text(ocr_text: str, target_language: str = "en") -> str:
    result = translate_text(ocr_text, target_language)
    translations = result.get("translations", [])
    if translations:
        return translations[0].get("text", "")
    return ""


def translate_multiple_texts(texts: list, target_language: str = "en") -> list:
    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    body = [{"text": t} for t in texts]
    headers = get_azure_translator_headers()

    response = requests.post(
        AZURE_TRANSLATOR_API_URL, params=params, headers=headers, json=body
    )
    response.raise_for_status()
    results = response.json()
    return [r["translations"][0]["text"] for r in results]


def detect_language(text: str) -> str:
    params = {"api-version": "3.0"}
    body = [{"text": text}]
    headers = get_azure_translator_headers()

    response = requests.post(
        AZURE_TRANSLATOR_ENDPOINT + "detect", params=params, headers=headers, json=body
    )
    response.raise_for_status()
    result = response.json()
    return result[0].get("language", "unknown")
