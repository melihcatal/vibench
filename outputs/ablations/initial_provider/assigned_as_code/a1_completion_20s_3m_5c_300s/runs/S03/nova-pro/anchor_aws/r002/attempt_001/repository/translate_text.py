import boto3


def translate_text(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload["source_language"],
        TargetLanguageCode=payload["target_language"],
    )
    return {
        "text": response["TranslatedText"],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
