import requests
import os


def translate_compliance_note(note: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    url = "https://api-free.deepl.com/v2/translate"
    params = {"auth_key": auth_key, "text": note, "target_lang": target_lang}
    response = requests.post(url, data=params)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]
