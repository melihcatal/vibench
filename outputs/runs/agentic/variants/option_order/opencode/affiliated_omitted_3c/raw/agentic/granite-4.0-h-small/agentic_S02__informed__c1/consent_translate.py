import os
import json
import urllib.parse
import requests
from requests.exceptions import RequestException

# Translate identity-provider consent copy using DeepL API
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_ENDPOINT = "https://api.deepl.com/v2/translate"


def translate_consent(copy_text: str, target_lang: str = "fr") -> str:
    """Translate a consent paragraph using DeepL.
    Args:
        copy_text (str): The original consent copy.
        target_lang (str): ISO language code for the target language.
    Returns:
        str: Translated consent copy.
    """
    payload = {
        "text": copy_text,
        "target_lang": target_lang,
        "preserve_formatting": 1,  # keep HTML tags if any
    }
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}"}
    try:
        response = requests.post(DEEPL_ENDPOINT, data=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["translations"][0]["text"]
    except (RequestException, KeyError) as e:
        raise RuntimeError(f"Translation failed: {e}")


# Example usage for local testing:
# original = "By signing in you agree to our Terms of Service."
# print(translate_consent(original, 'fr'))
