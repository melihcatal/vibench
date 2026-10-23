import os
import httpx


DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_onboarding_copy(text, target_locale, source_locale="en"):
    target_lang = target_locale.split("-")[0].upper()
    source_lang = source_locale.split("-")[0].upper()
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang,
        "source_lang": source_lang,
        "tag_handling": "html",
    }
    resp = httpx.post(DEEPL_API_URL, data=params)
    resp.raise_for_status()
    data = resp.json()
    translations = [t["text"] for t in data.get("translations", [])]
    return translations[0] if translations else text
