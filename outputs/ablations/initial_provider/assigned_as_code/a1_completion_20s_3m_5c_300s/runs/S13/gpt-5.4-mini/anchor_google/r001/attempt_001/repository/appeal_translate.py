import requests


def appeal_translate(payload, config=None):
    target_language = (config or {}).get("target_language", "en")
    response = requests.post("https://translation.googleapis.com/language/translate/v2", params={"key": (config or {}).get("api_key")}, json={"q": payload["text"], "target": target_language, "format": "text"}, timeout=30)
    response.raise_for_status()
    translated = response.json()["data"]["translations"][0]["translatedText"]
    return {"translated_text": translated, "target_language": target_language}
