from google.cloud import translate_v3 as translate
from security_models import RunbookTranslatePayload, TranslatedRunbookOutput

def runbook_translate(payload: RunbookTranslatePayload) -> TranslatedRunbookOutput:
    client = translate.TranslationServiceClient()

    parent = f"projects/{payload.project_id}/locations/global" # Global endpoint for translation

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload.text_to_translate],
            "target_language_code": payload.target_language,
            "source_language_code": payload.source_language if payload.source_language else None,
            "mime_type": "text/plain"  # Mime types: "text/plain" or "text/html"
        }
    )

    translated_text = ""
    detected_source_language = payload.source_language # Default to provided source language

    if response.translations:
        translated_text = response.translations[0].translated_text
        if not payload.source_language and response.translations[0].detected_language_code:
            detected_source_language = response.translations[0].detected_language_code

    return TranslatedRunbookOutput(
        original_text=payload.text_to_translate,
        translated_text=translated_text,
        target_language=payload.target_language,
        source_language=detected_source_language
    )
