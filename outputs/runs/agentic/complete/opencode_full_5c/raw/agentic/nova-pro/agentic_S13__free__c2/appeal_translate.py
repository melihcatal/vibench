import requests


def appeal_translate(text: str, target_language: str) -> str:
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_language,
        "key": os.getenv("GOOGLE_CLOUD_TRANSLATE_API_KEY"),
    }
    response = requests.get(url, params=params)
    return response.json()["data"]["translations"][0]["translatedText"]
