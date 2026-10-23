import boto3

from database_client import load_config


def record_translate(payload, config=None):
    load_config(config)
    translate = boto3.client("translate")
    text = payload["text"]
    source = payload.get("source_language", "auto")
    target = payload["target_language"]
    response = translate.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
    return {"text": response["TranslatedText"], "source_language": source, "target_language": target}
