from storage_client import get_translate_client
from storage_models import TranslateTextRequest, TranslateTextResponse

def translate_stored_text(request: TranslateTextRequest) -> TranslateTextResponse:
    """Translates text extracted from a stored document using Amazon Translate.

    Args:
        request: A TranslateTextRequest containing the text, source, and target language codes.

    Returns:
        A TranslateTextResponse with the translated text and language codes.
    """
    translate_client = get_translate_client()

    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code
    )

    translated_text = response['TranslatedText']
    source_language_code = response['SourceLanguageCode']
    target_language_code = response['TargetLanguageCode']

    return TranslateTextResponse(
        translated_text=translated_text,
        source_language_code=source_language_code,
        target_language_code=target_language_code
    )
