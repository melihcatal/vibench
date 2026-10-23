import requests


def consent_translate(payload, config=None):
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": (config or {}).get("api_key")},
        json={"q": payload["text"], "target": payload["target_language"], "format": "text"},
        timeout=30,
    )
    response.raise_for_status()
    translated = response.json()["data"]["translations"][0]["translatedText"]
    return {"translated_text": translated}
