import os
import hashlib
import uuid
import requests
from document_models import TranslationResult

AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "global")
AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"


def translate_ocr_text(
    text: str,
    target_language: str = "en",
    source_language: str | None = None,
) -> TranslationResult:
    if not text.strip():
        return TranslationResult(
            translated_text="",
            source_language=source_language or "",
            target_language=target_language,
        )

    path = "/translate"
    constructed_url = f"{AZURE_TRANSLATOR_ENDPOINT}{path}"

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]

    response = requests.post(
        constructed_url,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()
    result_data = response.json()

    translated = ""
    detected_source = source_language or ""
    confidence = 0.0

    if result_data and len(result_data) > 0:
        first_translation = result_data[0]
        if "translations" in first_translation and first_translation["translations"]:
            translated = first_translation["translations"][0].get("text", "")
        if "detectedLanguage" in first_translation:
            detected_source = first_translation["detectedLanguage"].get(
                "language", detected_source
            )
            confidence = first_translation["detectedLanguage"].get("score", 0.0)

    return TranslationResult(
        translated_text=translated,
        source_language=detected_source,
        target_language=target_language,
        confidence=confidence,
    )


def translate_ocr_text_batch(
    texts: list[str],
    target_language: str = "en",
    source_language: str | None = None,
) -> list[TranslationResult]:
    if not texts:
        return []

    path = "/translate"
    constructed_url = f"{AZURE_TRANSLATOR_ENDPOINT}{path}"

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": t} for t in texts if t.strip()]

    if not body:
        return [
            TranslationResult(
                translated_text="",
                source_language=source_language or "",
                target_language=target_language,
            )
            for _ in texts
        ]

    response = requests.post(
        constructed_url,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()
    result_data = response.json()

    results = []
    for idx, item in enumerate(result_data):
        translated = ""
        detected_source = source_language or ""
        confidence = 0.0
        if "translations" in item and item["translations"]:
            translated = item["translations"][0].get("text", "")
        if "detectedLanguage" in item:
            detected_source = item["detectedLanguage"].get("language", detected_source)
            confidence = item["detectedLanguage"].get("score", 0.0)
        results.append(
            TranslationResult(
                translated_text=translated,
                source_language=detected_source,
                target_language=target_language,
                confidence=confidence,
            )
        )

    return results
