import os
import requests


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def get_deepl_api_key() -> str:
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required")
    return api_key


def translate_appeal_text(appeal_text: str, target_lang: str = "EN") -> str:
    api_key = get_deepl_api_key()
    response = requests.post(
        DEEPL_API_URL,
        headers={
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "text": appeal_text,
            "target_lang": target_lang,
            "tag_handling": "xml",
        },
    )
    response.raise_for_status()
    result = response.json()
    translations = result.get("translations", [])
    if translations:
        return translations[0].get("text", "")
    return ""


def translate_appeal_batch(
    appeal_texts: list[str], target_lang: str = "EN"
) -> list[str]:
    api_key = get_deepl_api_key()
    response = requests.post(
        DEEPL_API_URL,
        headers={
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "text": appeal_texts,
            "target_lang": target_lang,
            "tag_handling": "xml",
        },
    )
    response.raise_for_status()
    result = response.json()
    translations = result.get("translations", [])
    return [t.get("text", "") for t in translations]


def detect_and_translate_appeal(appeal_text: str, target_lang: str = "EN") -> dict:
    api_key = get_deepl_api_key()
    detect_response = requests.post(
        "https://api.deepl.com/v2/translate",
        headers={
            "Authorization": f"DeepL-Auth-Key {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "text": appeal_text,
            "target_lang": target_lang,
        },
    )
    detect_response.raise_for_status()
    result = detect_response.json()
    translations = result.get("translations", [])
    translated = translations[0].get("text", "") if translations else ""
    detected_source = (
        translations[0].get("detected_source_language", "UNKNOWN")
        if translations
        else "UNKNOWN"
    )
    return {
        "original": appeal_text,
        "translated": translated,
        "detected_source_language": detected_source,
        "target_language": target_lang,
    }
