import os
from database_client import get_translate_client


def translate_record_field(
    text: str, source_language: str, target_language: str
) -> str:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
