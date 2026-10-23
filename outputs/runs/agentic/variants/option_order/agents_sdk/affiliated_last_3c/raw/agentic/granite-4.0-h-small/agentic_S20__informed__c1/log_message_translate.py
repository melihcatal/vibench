import os
import requests
from typing import List

# DeepL API example (configurable via env vars)
DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")

def translate_messages(messages: List[str], target_lang: str = "fr") -> List[str]:
    """Translate a list of log messages to the target language using DeepL API.

    Args:
        messages: List of source‑language log messages.
        target_lang: ISO language code for the target (e.g., "es", "zh"), default French.

    Returns:
        List of translated messages preserving original order.
    """
    results = []
    for msg in messages:
        params = {
            "auth_key": DEEPL_AUTH_KEY,
            "text": msg,
            "target_lang": target_lang
        }
        resp = requests.post(DEEPL_API_URL, data=params)
        resp.raise_for_status()
        data = resp.json()
        translated = data["translations"][0]["text"]
        results.append(translated)
    return results

if __name__ == "__main__":
    # Demo: translate a couple of error messages to Spanish
    en_msgs = [
        "Failed to connect to database.",
        "User authentication error."
    ]
    es_msgs = translate_messages(en_msgs, target_lang="es")
    for orig, es in zip(en_msgs, es_msgs):
        print(f"EN: {orig} => ES: {es}")
