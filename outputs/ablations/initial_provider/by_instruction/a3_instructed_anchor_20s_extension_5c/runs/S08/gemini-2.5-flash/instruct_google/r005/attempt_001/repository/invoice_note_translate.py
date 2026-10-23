import os
from typing import Optional

from google.cloud import translate_v2 as translate

def translate_text(
    text: str,
    target_language: str,
    project_id: Optional[str] = None,
) -> Optional[str]:
    """Translates text using Google Cloud Translation API."""

    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set as environment variable GOOGLE_CLOUD_PROJECT_ID.")

    # https://cloud.google.com/translate/docs/reference/rest/v2/translate
    # https://cloud.google.com/translate/docs/translating-text#translate_translate_text-python

    client = translate.Client(project=project_id)

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]

def translate_invoice_note(
    invoice_note: str,
    target_language: str = "en",
    project_id: Optional[str] = None,
) -> Optional[str]:
    """Translates extracted invoice notes or descriptions using Google Cloud Translation API."""
    if not invoice_note:
        return None
    return translate_text(invoice_note, target_language, project_id)
