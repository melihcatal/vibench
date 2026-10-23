import requests

from speech_client import load_config


def translate_script(text: str, target_language: str = "en") -> str:
    cfg = load_config()
    response = requests.post(
        "https://api.deepl.com/v2/translate",
        data={
            "auth_key": cfg.api_key,
            "text": text,
            "target_lang": target_language.upper(),
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["translations"][0]["text"]
