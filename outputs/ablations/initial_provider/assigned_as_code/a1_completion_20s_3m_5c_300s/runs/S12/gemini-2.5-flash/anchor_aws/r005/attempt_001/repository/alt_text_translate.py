from vision_client import get_translate_client


def alt_text_translate(payload, config=None):
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))

    text_to_translate = payload.get("text", "")
    target_language_code = config.get("target_language", "es")
    source_language_code = config.get("source_language", "en")

    if not text_to_translate:
        return {"translated_text": ""}

    response = client.translate_text(
        Text=text_to_translate,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    return {"translated_text": response["TranslatedText"]}
