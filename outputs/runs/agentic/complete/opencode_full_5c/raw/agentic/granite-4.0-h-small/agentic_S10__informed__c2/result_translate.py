import requests

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_to_english(text):
    """Translate text to English using DeepL API."""
    if not DEEPL_AUTH_KEY:
        raise RuntimeError("Set DEEPL_AUTH_KEY env var")
    url = "https://api.deepl.com/v2/translate"
    params = {"auth_key": DEEPL_AUTH_KEY, "text": text, "target_lang": "EN"}
    resp = requests.post(url, data=params)
    resp.raise_for_status()
    translated = resp.json()["translations"][0]["text"]
    return translated
