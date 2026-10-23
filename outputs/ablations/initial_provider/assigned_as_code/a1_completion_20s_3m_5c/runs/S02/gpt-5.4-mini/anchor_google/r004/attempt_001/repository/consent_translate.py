import requests


def consent_translate(payload, config=None):
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": payload.get("api_key", "")},
        json={"q": payload.get("text", ""), "target": payload.get("target_language", "es"), "format": "text"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()["data"]["translations"][0]
    return {"translated_text": data.get("translatedText"), "detected_source_language": data.get("detectedSourceLanguage")}
