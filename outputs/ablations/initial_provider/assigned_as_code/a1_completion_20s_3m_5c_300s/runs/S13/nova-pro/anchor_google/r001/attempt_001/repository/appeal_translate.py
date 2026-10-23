import os

import requests


def appeal_translate(text, target_language='es'):
    response = requests.post("https://translation.googleapis.com/language/translate/v2",
        params={"key": os.environ["GOOGLE_CLOUD_TRANSLATE_API_KEY"]},
        data={"q": text, "target": target_language})
    response.raise_for_status()
    return response.json()["data"]["translations"][0]["translatedText"]