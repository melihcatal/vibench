import requests


def dashboard_note_translate(payload, config=None):
    config = config or {}
    response = requests.post("https://translation.googleapis.com/language/translate/v2", params={"key": config.get("google_api_key", "")}, json={"q": payload["text"], "target": payload["target_locale"]}, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {"translated_text": data["data"]["translations"][0]["translatedText"], "provider": "google-translate"}
