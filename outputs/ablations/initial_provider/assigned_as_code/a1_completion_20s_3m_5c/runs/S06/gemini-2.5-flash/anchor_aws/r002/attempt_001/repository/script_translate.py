from speech_client import get_translate_client

def script_translate(payload, config=None):
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload.get("source_language_code", "auto"),
        TargetLanguageCode=payload["target_language_code"]
    )
    return {"translated_text": response["TranslatedText"]}
