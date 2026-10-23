import boto3


def result_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload["text"]
    source_language_code = payload.get("source_language", "auto")
    target_language_code = payload.get("target_language", "en")

    if source_language_code == "auto":
        translate_response = client.translate_text(
            Text=text,
            TargetLanguageCode=target_language_code
        )
    else:
        translate_response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
    
    translated_text = translate_response.get("TranslatedText", "")
    return {"translated_text": translated_text}
