import os
import requests


def localized_platform_output(output: str, target_locale: str = "FR") -> str:
    """
    Translates platform output using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": auth_key,
        "text": output,
        "target_lang": target_locale,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    result = response.json()
    return result["translations"][0]["text"]
