import os
import requests
from google.cloud.translate_v3 import TranslateTextRequest
from vision_client import VPCS_ENDPOINT, API_KEY

def translate_description(description, target_lang="es"):
    """Translate a generated image description to a target language using Google Cloud Translation API.
    Returns the translated caption. Uses API key if available; otherwise default client."
    if API_KEY:
        url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"
        data = {
            "q": description,
            "target": target_lang,
        }
        resp = requests.post(url, json=data)
        resp.raise_for_status()
        translated = resp.json()["data"]["translations"][0]["translatedText"]
        return translated
    # If no key, use default client (requires application-default credentials)
    client = TranslateTextRequest()
    # Placeholder: the real SDK usage would be more complex; here we just demonstrate intent.
    raise NotImplementedError("Direct SDK usage not implemented; use API key flow above.")
