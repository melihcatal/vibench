import requests


def translate_onboarding_copy(text, target_language):
    url = f"https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_language,
        "format": "text"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, params=params, headers=headers)
    if response.status_code == 200:
        translated_text = response.json()["data"]["translations"][0]["translatedText"]
        return translated_text
    else:
        return None