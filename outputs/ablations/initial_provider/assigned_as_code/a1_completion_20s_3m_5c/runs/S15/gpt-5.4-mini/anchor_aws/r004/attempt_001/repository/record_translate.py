import boto3

from database_models import build_response


def record_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    text = payload.get("text") or payload.get("document", {}).get("text") or ""
    translated = client.translate_text(
        Text=text,
        SourceLanguageCode=payload.get("source_language", config.get("source_language", "auto")),
        TargetLanguageCode=payload.get("target_language", config.get("target_language", "en")),
    )
    return build_response({"text": translated.get("TranslatedText"), "source_language": translated.get("SourceLanguageCode"), "target_language": translated.get("TargetLanguageCode")})
