import boto3

from vision_client import load_vision_config


def alt_text_translate(payload, config=None):
    config = load_vision_config(config)
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload.get("source_language", "en"),
        TargetLanguageCode=payload["target_language"],
    )
    return {"translated_text": response.get("TranslatedText", "")}
