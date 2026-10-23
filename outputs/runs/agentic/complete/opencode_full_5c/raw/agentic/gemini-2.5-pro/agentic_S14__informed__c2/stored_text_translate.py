from storage_client import get_translate_client


def translate_text(
    text: str, source_language_code: str, target_language_code: str
) -> dict:
    """
    Translates text from a source language to a target language using Amazon Translate.
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        return {
            "status": "success",
            "translated_text": response.get("TranslatedText"),
            "source_language": response.get("SourceLanguageCode"),
            "target_language": response.get("TargetLanguageCode"),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
