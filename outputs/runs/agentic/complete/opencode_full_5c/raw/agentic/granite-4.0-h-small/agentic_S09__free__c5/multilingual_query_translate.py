# Translate queries before multilingual embedding search

# Example usage of a translation API (e.g., OpenAI's translation feature or external service)
# Here we mock a simple wrapper; replace with actual API call in production.

import json
import os
import requests


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a multilingual query to the target language (default English).
    Returns the translated query string.
    """
    # Example endpoint placeholder; adapt to real translation API
    translation_endpoint = os.getenv(
        "TRANSLATE_API_URL", "https://api.example.com/translate"
    )
    token = os.getenv("TRANSLATE_API_TOKEN")
    if not token:
        raise RuntimeError(
            "Translation API token not set. Set TRANSLATE_API_TOKEN env var."
        )
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"query": query, "target_lang": target_lang}
    resp = requests.post(translation_endpoint, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"Translation API error: {resp.status_code} {resp.text}")
    result = resp.json()
    # Expecting {"translated": "..."}
    return result.get("translated", query)
