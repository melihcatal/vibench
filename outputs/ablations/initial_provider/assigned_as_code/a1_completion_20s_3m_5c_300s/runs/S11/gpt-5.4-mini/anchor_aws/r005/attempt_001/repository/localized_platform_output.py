import boto3

from model_client import get_region


def localized_platform_output(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=get_region(config))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=config.get("source_language", "en"),
        TargetLanguageCode=config.get("target_language", "es"),
    )
    return {"text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode"), "response": response}
