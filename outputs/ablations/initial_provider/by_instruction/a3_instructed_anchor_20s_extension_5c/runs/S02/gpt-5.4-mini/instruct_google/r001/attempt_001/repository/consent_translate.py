import requests


def consent_translate(text: str, target_language: str):
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"q": text, "target": target_language, "format": "text"},
        headers={"X-goog-api-key": ""},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
