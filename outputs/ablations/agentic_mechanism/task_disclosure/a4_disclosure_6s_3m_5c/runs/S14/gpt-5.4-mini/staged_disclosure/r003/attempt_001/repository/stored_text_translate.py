import os
import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_stored_text(text, target_lang, source_lang=None):
    api_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("Missing DeepL API key")
    data = {"text": text, "target_lang": target_lang}
    if source_lang:
        data["source_lang"] = source_lang
    response = requests.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    if not translations:
        raise RuntimeError("No translation returned by DeepL")
    return translations[0].get("text", "")
