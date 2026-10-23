from storage_client import get_translate_client
from storage_models import TranslateTextRequest, TranslateTextResponse


def translate_text(request: TranslateTextRequest) -> TranslateTextResponse:
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        return TranslateTextResponse(
            translated_text=response["TranslatedText"],
            source_language_code=response["SourceLanguageCode"],
            target_language_code=response["TargetLanguageCode"],
        )
    except Exception as e:
        raise RuntimeError(f"Failed to translate text: {e}")
