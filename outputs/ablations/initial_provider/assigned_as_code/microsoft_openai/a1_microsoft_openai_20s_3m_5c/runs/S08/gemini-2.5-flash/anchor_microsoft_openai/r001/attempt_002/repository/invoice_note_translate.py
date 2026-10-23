import os
from google.cloud import translate_v2 as translate

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    client = translate.Client()

    # Google Cloud Translation API does not require explicit project_id if GOOGLE_APPLICATION_CREDENTIALS is set
    # However, it's good practice to ensure project context if running in a GCP environment.
    # For this specific client, it implicitly uses the project from credentials or environment.

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
