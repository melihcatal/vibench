import boto3

from security_client import load_config


def runbook_translate(payload, config=None):
    config = load_config(config)
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(Text=payload["text"], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload["target_language"])
    return {"translated_text": response["TranslatedText"], "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode")}
