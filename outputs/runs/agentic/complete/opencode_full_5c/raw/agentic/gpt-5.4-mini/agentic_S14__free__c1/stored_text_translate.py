from storage_client import get_translate_client


def stored_text_translate(
    text: str, source_language_code: str = "auto", target_language_code: str = "en"
):
    translate = get_translate_client()
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code,
    )
    return {
        "translated_text": response.get("TranslatedText"),
        "source_language_code": response.get("SourceLanguageCode"),
        "target_language_code": response.get("TargetLanguageCode"),
    }
