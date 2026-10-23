from storage_client import get_translate_client
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def translate_stored_text(
    request: StoredTextTranslateRequest,
) -> StoredTextTranslateResponse:
    """Translates text extracted from a stored document using AWS Translate."""
    translate_client = get_translate_client()

    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code,
    )

    return StoredTextTranslateResponse(
        translated_text=response['TranslatedText'],
        source_language_code=response['SourceLanguageCode'],
        target_language_code=response['TargetLanguageCode'],
    )
