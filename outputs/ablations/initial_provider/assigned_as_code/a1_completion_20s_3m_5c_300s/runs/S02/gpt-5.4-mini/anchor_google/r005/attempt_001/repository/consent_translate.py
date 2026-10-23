import requests


def consent_translate(payload, config=None):
    config = dict(config or {})
    response = requests.post("https://translation.googleapis.com/language/translate/v2",
                             params={"key": config["api_key"]}, json={"q": payload["text"], "target": payload["target_language"], "format": "text"}, timeout=30)
    response.raise_for_status()
    result = response.json()
    translated = result.get("data", {}).get("translations", [{}])[0].get("translatedText")
    return {"source_text": payload["text"], "translated_text": translated, "target_language": payload["target_language"]}
