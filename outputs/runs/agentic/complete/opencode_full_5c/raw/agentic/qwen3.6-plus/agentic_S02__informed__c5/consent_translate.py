import os
import time
import requests
from identity_client import DEEPL_AUTH_KEY, DEEPL_API_URL
from identity_models import TranslationResult


def translate_consent_text(
    text, target_lang, source_lang=None, api_key=None, api_url=None
):
    if not api_key:
        api_key = DEEPL_AUTH_KEY
    if not api_url:
        api_url = DEEPL_API_URL
    if not text or not text.strip():
        return TranslationResult(
            translated_text="",
            source_language=source_lang or "auto",
            target_language=target_lang,
            provider="deepl",
        )
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "text": text,
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        payload["source_lang"] = source_lang.upper()
    response = requests.post(api_url, data=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    translated_text = ""
    detected_source = source_lang or "auto"
    if translations:
        translated_text = translations[0].get("text", "")
        detected_source = translations[0].get(
            "detected_source_language", detected_source
        )
    return TranslationResult(
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_lang,
        provider="deepl",
    )


def translate_consent_batch(
    texts, target_lang, source_lang=None, api_key=None, api_url=None
):
    if not api_key:
        api_key = DEEPL_AUTH_KEY
    if not api_url:
        api_url = DEEPL_API_URL
    if not texts:
        return []
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "text": texts,
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        payload["source_lang"] = source_lang.upper()
    response = requests.post(api_url, data=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    results = []
    for i, t in enumerate(translations):
        results.append(
            TranslationResult(
                translated_text=t.get("text", ""),
                source_language=t.get(
                    "detected_source_language", source_lang or "auto"
                ),
                target_language=target_lang,
                provider="deepl",
            )
        )
    return results


def translate_idp_consent(
    consent_text, target_languages, source_lang=None, api_key=None, api_url=None
):
    all_results = {}
    for lang in target_languages:
        result = translate_consent_text(
            consent_text, lang, source_lang, api_key, api_url
        )
        all_results[lang] = result
    return all_results
