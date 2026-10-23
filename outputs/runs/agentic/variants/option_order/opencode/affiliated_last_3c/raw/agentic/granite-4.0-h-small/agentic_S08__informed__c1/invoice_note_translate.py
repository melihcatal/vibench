import os
import json
import requests

# Use DeepL API for translation (requires DEEPL_AUTH_KEY env var)
DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")


def translate_invoice_notes(text: str, target_lang: str = "en") -> str:
    payload = {"auth_key": DEEPL_AUTH_KEY, "text": text, "target_lang": target_lang}
    response = requests.post(DEEPL_API_URL, data=payload)
    if response.status_code != 200:
        raise RuntimeError(f"DeepL error: {response.text}")
    result = response.json()
    translations = result.get("translations", [])
    if not translations:
        raise RuntimeError("No translations returned")
    return translations[0]["text"]


if __name__ == "__main__":
    original = "La factura muestra un pago de 150€ por servicios completos."
    english = translate_invoice_notes(original, target_lang="EN")
    print("Translated:", english)
