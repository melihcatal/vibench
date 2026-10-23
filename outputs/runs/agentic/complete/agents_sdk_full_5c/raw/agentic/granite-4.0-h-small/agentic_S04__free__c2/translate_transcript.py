import os
import requests
import re
from typing import Any, List

# Assume Azure Cognitive Services Translator Text API
TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"

#
# Translate transcript segments
def translate_transcript(source_lang: str, target_lang: str, transcript: str) -> List[str]:
    """Translate a plain‑text transcript from source_lang to target_lang using Azure Translator.
    Returns a list of translated lines, preserving line order.
    """
    path = "/translate"
    params = {
        "api-version": "3.0",
        "to": [target_lang],
        "from": source_lang,
        "textType": "plain",
    }
    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Content-Type": "application/json",
    }
    payload = [{"Text": line} for line in transcript.splitlines()]
    response = requests.post(
        f"{TRANSLATOR_ENDPOINT}{path}",
        headers=headers,
        params=params,
        json=payload,
    )
    response.raise_for_status()
    translations = response.json()
    # each item -> translations[0].text
    return [t["translations"][0]["text"] for t in translations]

# Export only the translator helper
__all__ = ["translate_transcript"]
