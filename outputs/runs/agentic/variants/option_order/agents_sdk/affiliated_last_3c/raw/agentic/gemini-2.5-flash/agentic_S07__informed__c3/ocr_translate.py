import os
from google.cloud import translate_v3beta1 as translate
from document_models import TranslatedTextResult

def translate_ocr_text(text: str, target_language: str, project_id: str = None, source_language: str = None) -> TranslatedTextResult:
    """
    Translates extracted OCR text using Google Cloud Translation.
    project_id is optional; if not provided, it will attempt to use GOOGLE_CLOUD_PROJECT env var.
    """
    client = translate.TranslationServiceClient()

    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language, # Optional: if not provided, it will auto-detect
        model="projects/{}/locations/global/models/general/nmt".format(project_id) # Using NMT model
    )

    translated_text = ""
    detected_source_language = ""

    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

    return TranslatedTextResult(
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=target_language
    )
