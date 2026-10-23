import os
from observability_client import get_translation_client
from google.cloud.translate_v3 import types

# Google Cloud project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def translate_dashboard_note(
    text: str,
    target_language_code: str,
    project_id: str,
    source_language_code: str = None,
) -> dict:
    """Translates metric or dashboard notes for another locale using Google Cloud Translation API."""
    client = get_translation_client()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code, # Optional: if not provided, auto-detects
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else ""
    detected_source_language = response.translations[0].detected_language_code if response.translations else ""

    return {
        "original_text": text,
        "translated_text": translated_text,
        "target_language_code": target_language_code,
        "detected_source_language_code": detected_source_language,
        "provider": "Google Cloud Translation API", # Provider identifying signal
    }

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # note_en = "The CPU utilization is spiking due to a new deployment."
    # note_es = "La utilización de la CPU está aumentando debido a una nueva implementación."

    # translated_note_es = translate_dashboard_note(note_en, "es", PROJECT_ID)
    # print("English to Spanish:", translated_note_es)

    # translated_note_en = translate_dashboard_note(note_es, "en", PROJECT_ID)
    # print("Spanish to English:", translated_note_en)
    pass
