from database_client import get_translate_client

def record_translate(text: str, source_language_code: str, target_language_code: str) -> str:
    """
    Translates user-facing document fields using AWS Translate.
    """
    translate = get_translate_client()

    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    translated_text = response.get("TranslatedText", "")
    return translated_text
