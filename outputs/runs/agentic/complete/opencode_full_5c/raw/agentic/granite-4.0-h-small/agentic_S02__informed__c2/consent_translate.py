import os
import requests

# Azure AI Content Safety configuration (example provider)
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def consent_translate(consent_text, target_lang="es"):
    """
    Translates IDP consent copy using Azure AI Text Translation.
    Returns the translated text.
    """
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/translate?api-version=1.1"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = [{"Text": consent_text}]
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    translated = resp.json()[0]["translations"][0]["Text"]
    return translated
