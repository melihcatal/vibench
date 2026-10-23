import os
import requests


def translate_log_message(log_message: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    url = "https://api-free.deepl.com/v2/translate"
    data = {"auth_key": auth_key, "text": log_message, "target_lang": target_lang}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]


if __name__ == "__main__":
    english_log = "Failed to process payment due to invalid card details."
    spanish_log = translate_log_message(english_log, "ES")
    print(f"Original: {english_log}")
    print(f"Translated: {spanish_log}")
