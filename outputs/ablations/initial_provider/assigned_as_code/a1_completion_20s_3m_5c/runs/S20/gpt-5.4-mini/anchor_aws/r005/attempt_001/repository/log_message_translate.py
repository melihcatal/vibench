import boto3


def log_message_translate(text, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(Text=text, SourceLanguageCode=config.get("source_language", "auto"), TargetLanguageCode=config.get("target_language", "es"))
    return {"translated_text": response.get("TranslatedText"), "target_language": config.get("target_language", "es")}
