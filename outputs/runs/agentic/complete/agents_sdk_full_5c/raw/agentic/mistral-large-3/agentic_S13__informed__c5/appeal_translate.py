# Translate appeal text for review using Azure AI Translator

import os
import requests
from typing import Dict


def translate_appeal_text(text: str, target_language: str) -> str:
    """Translate appeal text for review using Azure AI Translator."""
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    endpoint = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}"
    
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }
    payload = [{"text": text}]
    
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]