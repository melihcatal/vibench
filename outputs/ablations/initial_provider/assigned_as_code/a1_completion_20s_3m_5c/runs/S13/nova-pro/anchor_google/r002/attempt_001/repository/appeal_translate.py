import os

import requests


def appeal_translate(text, target_language, config=None):
    client_id = config.get("client_id") or os.environ["GOOGLE_CLOUD_TRANSLATE_CLIENT_ID"]
    client_secret = config.get("client_secret") or os.environ["GOOGLE_CLOUD_TRANSLATE_CLIENT_SECRET"]
    response = requests.post("https://translation.googleapis.com/language/translate/v2",
        params={"q": text, "target": target_language},
        auth=(client_id, client_secret), timeout=30)
    response.raise_for_status()
    return response.json()["data"]["translations"][0]["translatedText"]