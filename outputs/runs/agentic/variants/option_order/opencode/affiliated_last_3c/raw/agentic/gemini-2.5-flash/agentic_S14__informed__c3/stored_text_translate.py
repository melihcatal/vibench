from google.cloud import translate_v2 as translate
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse


def translate_stored_text(
    request: StoredTextTranslateRequest,
) -> StoredTextTranslateResponse:
    """Translates text extracted from a stored document using Google Cloud Translation."""
    client = translate.Client()

    # Target language must be provided
    if not request.target_language:
        raise ValueError("Target language must be specified.")

    result = client.translate(
        request.text_content,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return StoredTextTranslateResponse(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
        target_language=request.target_language,
    )
