import boto3

from vision_client import load_config


def alt_text_translate(payload, config=None):
    config = load_config(config)
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload.get("description", "") if isinstance(payload, dict) else ""
    target = config.get("language", "en")
    response = client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target)
    return {"translated_text": response.get("TranslatedText", "")}
