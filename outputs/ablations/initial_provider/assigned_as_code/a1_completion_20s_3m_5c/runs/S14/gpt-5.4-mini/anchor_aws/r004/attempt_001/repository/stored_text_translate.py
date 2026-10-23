import boto3

from storage_models import encode_text


def stored_text_translate(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(Text=payload["text"], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=payload["target_language"])
    return {"translated_text": response.get("TranslatedText"), "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode"), "encoded": encode_text(response.get("TranslatedText"))}
