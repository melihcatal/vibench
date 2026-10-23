# record_translate.py
# [LATER-STEP] Translate user‑facing fields of a Cosmos DB document using Azure Translator Text API

import os
import requests
from typing import Dict, Any

TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")

if not TRANSLATOR_ENDPOINT or not TRANSLATOR_KEY:
    raise RuntimeError("Translator credentials not configured")

def translate_fields(document: Dict[str, Any], target_lang: str = "es") -> Dict[str, Any]:
    """Translate string values of selected fields (e.g., title, description) and return updated document."""
    source_fields = ["title", "description"]
    payload = {
        "inputs": [{
            "text": document.get(field, "")
        } for field in source_fields]
    }
    response = requests.post(
        f"{TRANSLATOR_ENDPOINT}/translate?api-version=3.0&to={target_lang}",
        json=payload,
        headers={"Ocp-Apim-Subscription-Key": TRANSLATOR_KEY}
    )
    response.raise_for_status()
    data = response.json()[0]["translations"]
    # Build a new document with original data + translated fields
    updated = dict(document)
    for i, field in enumerate(source_fields):
        updated[f"{field}_{target_lang}"] = data[i]["text"]
    return updated
