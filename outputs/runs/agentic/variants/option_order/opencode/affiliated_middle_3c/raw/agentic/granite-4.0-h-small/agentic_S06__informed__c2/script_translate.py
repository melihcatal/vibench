import os
import json
from typing import Dict, Any
import requests

# DeepL translation API (example provider)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_ENDPOINT = "https://api.deepl.com/v2/translate"


def translate_script(text: str, target_lang: str = "de") -> Dict[str, Any]:
    """Translate plain text using DeepL.

    Args:
        text: Source narration script.
        target_lang: ISO language code (e.g., 'de' for German).

    Returns:
        JSON response from DeepL containing translated text.
    """
    payload = {"auth_key": DEEPL_AUTH_KEY, "text": text, "target_lang": target_lang}
    resp = requests.post(DEEPL_ENDPOINT, data=payload)
    resp.raise_for_status()
    return resp.json()


# Example usage (remove in production)
if __name__ == "__main__":
    sample = "Hello world, this is a test script."
    print(translate_script(sample, target_lang="es"))
