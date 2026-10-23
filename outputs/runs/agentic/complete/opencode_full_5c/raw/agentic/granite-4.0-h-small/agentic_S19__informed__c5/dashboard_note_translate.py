# dashboard_note_translate.py
# LATER-STEP implementation using Datadog Metrics API for fetching notes and Azure Translator for translation

import os
from typing import List
from observability_client import ObservabilityClient
from observability_models import TranslateRequest, TranslateResponse
from azure.ai.translation.text import TranslateClient

# Provider identifier for this file (visible in code)
PROVIDER = "datadog"


def translate_dashboard_notes(req: TranslateRequest) -> TranslateResponse:
    client = ObservabilityClient()
    # NOTE: Datadog does not expose dashboard notes via the Metrics API.
    # This example assumes you have a separate endpoint or key-value store that holds notes.
    # For demonstration, we simulate fetching notes as a list of strings.
    notes = client.query_recent(metric_name="dummy_metric", start="now-1h", end="now")
    # Placeholder replacement - replace with real fetch if available
    texts = req.texts
    # Step 2: Translate each text using Azure Translator
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    client = TranslateClient(endpoint=endpoint, credential=key)
    translations = client.translate(texts, target_language=req.target_locale)
    return TranslateResponse(target_locale=req.target_locale, translations=translations)


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    req = TranslateRequest(
        source_locale="en",
        target_locale="fr",
        texts=["CPU usage is high", "Database lag detected"],
    )
    result = translate_dashboard_notes(req)
    print(result)
