import os
from document_models import TranslationResult
from document_client import get_translation_client

def translate_invoice_note(text: str, target_language_code: str, config: dict = None) -> TranslationResult:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    client = get_translation_client()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslationResult(translated_text=translated_text)
