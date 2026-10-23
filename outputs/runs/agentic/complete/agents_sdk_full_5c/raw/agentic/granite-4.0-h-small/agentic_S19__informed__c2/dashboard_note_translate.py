import os
import requests
from datetime import datetime
from observability_client import get_cloudwatch_client
from observability_models import MetricStatisticsRequest

def translate_dashboard_notes(source_locale, target_locale, note_texts):
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API (REST)."
    # Ensure credentials are available
    gcp_cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not gcp_cred:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS env variable not set")
    # Cloud Translation endpoint (REST)
    endpoint = "https://translation.googleapis.com/v3/projects/-/locations/global:translateText"
    headers = {
        "Authorization": f"Bearer $(gcloud auth print-access-token)",
        "Content-Type": "application/json"
    }
    # In a real script you would acquire the access token via gcloud CLI.
    # Here we simulate a successful call by directly using requests.
    # The note_texts parameter is a dict: {note_id: note_content}
    translations = {}
    for note_id, text in note_texts.items():
        payload = {
            "sourceLanguageCode": source_locale,
            "targetLanguageCode": target_locale,
            "contents": [text]
        }
        resp = requests.post(endpoint, json=payload, headers=headers)
        resp.raise_for_status()
        result = resp.json()
        translations[note_id] = result["translatedTexts"][0]["text"]
    return translations

if __name__ == "__main__":
    # Example: translate two dashboard notes from English to Spanish.
    example_notes = {
        "note_1": "High CPU utilization observed",
        "note_2": "Check for potential memory leaks"
    }
    translated = translate_dashboard_notes(
        source_locale="en",
        target_locale="es",
        note_texts=example_notes
    )
    print("Translated notes:", translated)
