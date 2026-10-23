# [LATER-STEP] welcome_translate.py
# Translate onboarding copy into the user's locale

# Example integration using DeepL API for translation (concrete provider)

DEEPL_AUTH_KEY = os.getenv(
    "DEEPL_AUTH_KEY"
)  # <-- set your DeepL API key in the environment
BASE_URL = "https://api.deepl.com/v2"

import json
import requests


def translate_welcome(text: str, target_lang: str = "EN") -> str:
    """Translate a welcome message using DeepL's translate endpoint.
    Returns the translated text.
    """
    if not DEEPL_AUTH_KEY:
        raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")
    payload = {"auth_key": DEEPL_AUTH_KEY, "text": text, "target_lang": target_lang}
    response = requests.post(f"{BASE_URL}/translate", data=payload)
    response.raise_for_status()
    data = response.json()
    # DeepL returns translations in data['translations'][0]['text']
    return data["translations"][0]["text"]


# Example usage:
# translated = translate_welcome("Welcome to the platform!", target_lang="ES")
