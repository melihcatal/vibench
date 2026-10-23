import requests


def consent_translate(payload, config=None):
    response = requests.post("https://translation.googleapis.com/language/translate/v2", params={"key": config["google_translate_api_key"]}, json={"q": payload["text"], "target": payload["target_language"]}, timeout=30)
    response.raise_for_status()
    return response.json()
