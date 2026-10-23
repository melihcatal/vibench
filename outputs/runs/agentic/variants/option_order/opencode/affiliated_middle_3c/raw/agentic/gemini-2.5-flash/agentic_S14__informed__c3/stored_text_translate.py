from storage_client import get_translate_client
from storage_models import TranslateTextRequest, TranslateTextResponse


def translate_extracted_text(request: TranslateTextRequest) -> TranslateTextResponse:
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        translated_text = response.get("TranslatedText")
        return TranslateTextResponse(
            success=True,
            message="Text translated successfully.",
            translated_text=translated_text,
        )
    except Exception as e:
        return TranslateTextResponse(
            success=False, message=f"Error translating text: {str(e)}"
        )
