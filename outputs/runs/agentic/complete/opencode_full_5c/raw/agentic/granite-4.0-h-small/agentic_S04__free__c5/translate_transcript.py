import os
import requests

# provider: DeepL API (concrete HTTP endpoint)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
API_URL = "https://api.deepl.com/v2/translate"


def translate_transcript(transcript, target_lang="FR"):
    """
    Translate a plain text transcript using DeepL.
    Returns translated text.
    """
    payload = {"text": transcript, "target_lang": target_lang}
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}"}
    response = requests.post(API_URL, data=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]
