import boto3

from storage_client import load_storage_config


def stored_text_translate(payload, config=None):
    cfg = load_storage_config(config)
    client = boto3.client("translate", region_name=cfg["region"])
    text = payload.get("text", "")
    source_language = payload.get("source_language", cfg.get("language", "en"))
    target_language = payload.get("target_language", "en")
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return {"text": text, "translated_text": response.get("TranslatedText", ""), "source_language": source_language, "target_language": target_language}
