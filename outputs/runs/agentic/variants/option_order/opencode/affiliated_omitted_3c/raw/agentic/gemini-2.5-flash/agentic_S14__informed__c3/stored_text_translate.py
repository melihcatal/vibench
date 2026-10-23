from storage_client import get_translate_client
from storage_models import TextTranslateRequest, TextTranslateResponse


def translate_stored_text(request: TextTranslateRequest) -> TextTranslateResponse:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language,
        TargetLanguageCode=request.target_language,
    )
    return TextTranslateResponse(
        translated_text=response["TranslatedText"], raw_response=response
    )
