from storage_client import get_translate_client
from storage_models import TranslateRequest


def translate_text(request: TranslateRequest) -> str:
    """
    Translates text using Amazon Translate.
    """
    translate_client = get_translate_client()

    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code,
    )

    return response.get("TranslatedText", "")
