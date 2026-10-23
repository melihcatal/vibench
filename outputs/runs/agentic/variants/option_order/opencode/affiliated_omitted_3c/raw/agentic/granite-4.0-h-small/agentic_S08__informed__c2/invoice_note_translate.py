import os
import json
import http.client

google_translate_api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")


def translate_note(text: str, target_lang: str = "es") -> str:
    """
    Translate extracted invoice notes or descriptions using Google Cloud Translation API.
    Returns the translated string.
    """
    endpoint = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_lang,
        "format": "text",
        "key": google_translate_api_key,
    }
    conn = http.client.HTTPSConnection("translation.googleapis.com", timeout=10)
    conn.request("GET", f"{endpoint}?{params.asis()}")  # using query string formatting
    resp = conn.getresponse()
    raw = resp.read().decode()
    data = json.loads(raw)
    translated = data["data"]["translations"][0]["translatedText"]
    conn.close()
    return translated
