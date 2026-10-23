from messaging_client import get_translate_client

def payload_translate(text, source_language_code, target_language_code, config=None):
    config = config or {}
    translate_client = get_translate_client(config.get("region"))

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    return {"translated_text": response["TranslatedText"], "source_language": response["SourceLanguageCode"], "target_language": response["TargetLanguageCode"]}
