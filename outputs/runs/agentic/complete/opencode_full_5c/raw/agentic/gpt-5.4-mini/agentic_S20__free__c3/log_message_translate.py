import requests


def translate_log_message(text: str, target_locale: str = "es") -> dict:
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": None},
        json={"q": text, "target": target_locale},
        timeout=10,
    )
    return response.json()
