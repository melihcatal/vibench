import os
import requests

DEEPL_API_BASE = os.getenv("DEEPL_API_BASE", "https://api-free.deepl.com/v2")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")


def dashboard_note_translate(text, target_lang="EN-US"):
    if not DEEPL_API_KEY:
        return {"translated_text": text, "warning": "missing DEEPL_API_KEY"}
    data = {"auth_key": DEEPL_API_KEY, "text": text, "target_lang": target_lang}
    r = requests.post(f"{DEEPL_API_BASE}/translate", data=data, timeout=30)
    r.raise_for_status()
    return r.json()
