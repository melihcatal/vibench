import requests


def dashboard_note_translate(text, target_language):
    endpoint = "https://translation.googleapis.com/language/translate/v2"
    params = {"q": text, "target": target_language, "key": "${GOOGLE_API_KEY}"}
    response = requests.get(endpoint, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
