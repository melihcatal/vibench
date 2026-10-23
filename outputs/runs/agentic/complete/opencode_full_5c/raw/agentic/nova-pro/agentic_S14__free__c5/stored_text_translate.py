import boto3
from storage_client import get_translate_client
from storage_models import TranslateResponse


def stored_text_translate(text, source_language_code, target_language_code):
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return TranslateResponse(response["TranslatedText"])
