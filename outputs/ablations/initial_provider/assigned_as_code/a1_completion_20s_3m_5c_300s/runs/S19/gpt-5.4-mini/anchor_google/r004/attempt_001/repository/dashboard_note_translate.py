import requests


def dashboard_note_translate(payload, config=None):
    api_key = (config or {}).get("api_key")
    if not api_key:
        raise ValueError("api_key is required")
    response = requests.post("https://translation.googleapis.com/language/translate/v2", params={"key": api_key}, json={"q": payload["text"], "target": payload["target_language"], "format": "text"}, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {"translated_text": data["data"]["translations"][0]["translatedText"]}
