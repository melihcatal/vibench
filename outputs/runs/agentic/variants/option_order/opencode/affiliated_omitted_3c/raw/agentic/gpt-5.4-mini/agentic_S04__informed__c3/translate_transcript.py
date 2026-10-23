import requests

from speech_client import get_env


def translate_transcript(text: str = "", target_language: str = "ES"):
    api_key = get_env("DEEPL_AUTH_KEY")
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={"auth_key": api_key, "text": text, "target_lang": target_language},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
