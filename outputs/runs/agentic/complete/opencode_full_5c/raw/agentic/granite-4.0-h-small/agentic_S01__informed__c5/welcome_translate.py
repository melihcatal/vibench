# welcome_translate.py - Translate onboarding copy into the user's locale
# Using Azure AI Translator as the concrete provider

import os
import requests
from typing import List, Dict

TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")

BASE_URL = f"https://{TRANSLATOR_ENDPOINT}.cognitiveservices.azure.com/"
VERSION = "v3.0"
TRANSLATE_PATH = f"{VERSION}/translate"


def translate_text(texts: List[str], target_locale: str) -> List[Dict[str, str]]:
    """Translate a list of strings to the specified target locale.",

    Returns a list of dictionaries with the translated text and detected source language.",

    Uses the Azure AI Translator REST API.",
    """
    url = BASE_URL + TRANSLATE_PATH
    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Content-Type": "application/json",
    }
    body = [
        {
            "Text": txt,
            "To": target_locale,
        }
        for txt in texts
    ]
    resp = requests.post(url, headers=headers, json=body)
    resp.raise_for_status()
    result = resp.json()
    return [
        {
            "source_language": entry["detectedLanguage"]["language"],
            "translated_text": entry["translations"][0]["text"],
        }
        for entry in result
    ]
