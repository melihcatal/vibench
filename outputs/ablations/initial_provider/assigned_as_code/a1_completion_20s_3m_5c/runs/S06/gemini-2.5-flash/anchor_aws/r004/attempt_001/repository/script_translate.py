from speech_client import get_translate_client


def script_translate(text, source_language_code, target_language_code, config=None):
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return {"translated_text": response["TranslatedText"], "source_language": response["SourceLanguageCode"], "target_language": response["TargetLanguageCode"]}
