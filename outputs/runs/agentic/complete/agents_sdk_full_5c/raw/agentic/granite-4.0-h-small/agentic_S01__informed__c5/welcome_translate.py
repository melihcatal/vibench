import os
import requests
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Azure AI Translator as the provider for text translation
AZURE_TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')

TRANSLATOR_URI = f"{AZURE_TRANSLATOR_ENDPOINT}/translate"

HEADERS = {
    "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def translate_welcome(original_text: str, target_locale: str) -> str:
    """Translate onboarding welcome copy into the user's locale.

    Uses Azure AI Translator's v3 API.
    Returns the translated string.
    Raises IdentityError on API failure.
    """
    payload = [
        {
            "Text": original_text,
        }
    ]
    params = {
        "api-version": "3.0",
        "to": [target_locale],
    }
    response = requests.post(TRANSLATOR_URI, headers=HEADERS, params=params, json=payload)
    if response.status_code != 200:
        raise IdentityError(f"Translation failed: {response.text}")
    # Azure returns a list of objects with a 'translations' key
    try:
        translations = response.json()[0]["translations"]
        translated_text = translations[0]["text"]
        return translated_text
    except (KeyError, IndexError, TypeError):
        raise IdentityError(f"Unexpected translation payload: {response.text}")
