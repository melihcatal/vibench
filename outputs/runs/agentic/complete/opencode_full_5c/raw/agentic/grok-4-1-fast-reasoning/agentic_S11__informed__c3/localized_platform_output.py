import os
import requests


def localize_platform_output(text: str, target_lang: str = "FR") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang,
    }
    resp = requests.post(url, data=data)
    if resp.status_code == 200:
        return resp.json()["translations"][0]["text"]
    else:
        raise ValueError(f"DeepL API error: {resp.text}")
