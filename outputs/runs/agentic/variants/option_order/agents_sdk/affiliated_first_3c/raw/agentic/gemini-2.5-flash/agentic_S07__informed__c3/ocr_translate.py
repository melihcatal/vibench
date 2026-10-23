import os
from google.cloud import translate_v3 as translate
from document_models import TranslationResponse

def translate_text(
    text: str,
    target_language_code: str,
    project_id: str,
    location: str = "global",
) -> TranslationResponse:
    """
    Translates extracted OCR text using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
        
    return TranslationResponse(translated_text=translated_text)

