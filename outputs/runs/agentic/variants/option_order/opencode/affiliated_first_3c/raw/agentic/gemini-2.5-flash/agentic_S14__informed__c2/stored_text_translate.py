from storage_client import get_translate_client


def translate_extracted_text(
    text: str, source_language_code: str, target_language_code: str
) -> str:
    """
    Translates text extracted from a stored document using Amazon Translate.
    """
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return response["TranslatedText"]
