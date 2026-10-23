import os
import requests


def dashboard_note_translate(text, target_locale="es"):
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    response = requests.post("https://api-free.deepl.com/v2/translate", data={"auth_key": auth_key, "text": text, "target_lang": target_locale.upper()}, timeout=30)
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    return translations[0].get("text", text) if translations else text
