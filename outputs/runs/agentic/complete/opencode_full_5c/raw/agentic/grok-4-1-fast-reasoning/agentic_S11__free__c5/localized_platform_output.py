import os
import requests


def localized_platform_output(content: str, target_locale: str = "FR") -> str:
    """
    Translates platform model output to another locale using DeepL.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set")
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": auth_key,
        "text": content,
        "target_lang": target_locale,
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    data = response.json()
    if "translations" not in data:
        raise ValueError(f"DeepL API error: {data}")
    return data["translations"][0]["text"]
