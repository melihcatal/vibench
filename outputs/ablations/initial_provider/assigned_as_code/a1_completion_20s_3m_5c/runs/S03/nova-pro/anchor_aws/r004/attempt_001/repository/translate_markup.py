import boto3


def translate_markup(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload["text"]
    source_language = payload["source_language"]
    target_language = payload["target_language"]
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return {
        "text": response["TranslatedText"],
        "source_language": source_language,
        "target_language": target_language,
    }