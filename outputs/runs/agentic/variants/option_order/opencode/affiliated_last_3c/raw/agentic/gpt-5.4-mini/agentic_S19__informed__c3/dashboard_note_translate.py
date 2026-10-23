import os

import requests


def dashboard_note_translate(text, target_locale):
    key = os.getenv("DEEPL_AUTH_KEY", "")
    if not key:
        return {"translated_text": text, "locale": target_locale, "provider": "deepl"}
    resp = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={"auth_key": key, "text": text, "target_lang": target_locale.upper()},
        timeout=30,
    )
    data = resp.json()
    translated = data.get("translations", [{}])[0].get("text", text)
    return {"translated_text": translated, "locale": target_locale, "provider": "deepl"}
