# [LATER-STEP] multilingual_query_translate.py
# Translate queries before multilingual embedding search

# Provider: Azure AI Translator (REST API) – identifiable via endpoint and key
# Integration signal: AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables

import os
import requests
from typing import Tuple

AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")

if not (AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION):
    raise RuntimeError(
        "Set AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables"
    )


def translate_query(query: str, target_lang: str = "es") -> Tuple[str, dict]:
    """Translate a query string to the target language using Azure Translator.
    Returns the translated text and the raw response dict.
    """
    url = f"{AZURE_TRANSLATOR_ENDPOINT}/{AZURE_TRANSLATOR_REGION}/translate?api-version=3.0&to={target_lang}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Content-Type": "application/json",
    }
    payload = [{"Text": query}]
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()[0]
    translated_text = result["translations"][0]["text"]
    return translated_text, resp.json()
