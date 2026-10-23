from google.cloud import translate_v2 as translate
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def translate_stored_text(payload: StoredTextTranslateRequest, config=None):
    config = config or {}
    translate_client = translate.Client(project=config["project_id"])

    if payload.source_language_code == "auto":
        result = translate_client.translate(
            payload.text_content,
            target_language=payload.target_language_code
        )
    else:
        result = translate_client.translate(
            payload.text_content,
            source_language=payload.source_language_code,
            target_language=payload.target_language_code,
        )

    return StoredTextTranslateResponse(
        translated_text=result["translatedText"],
        source_language_code=result["detectedSourceLanguage"],
        target_language_code=payload.target_language_code,
    )
