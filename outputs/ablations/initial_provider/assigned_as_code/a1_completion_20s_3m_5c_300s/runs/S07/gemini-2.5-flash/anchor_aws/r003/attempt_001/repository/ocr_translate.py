import boto3
from document_client import get_translate_client


def ocr_translate(payload, config=None):
    config = config or {}
    client = get_translate_client(region_name=config.get("region"))
    text_to_translate = payload["text"]
    source_language = payload.get("source_language", "auto")
    target_language = payload.get("target_language", "en")

    if source_language == "auto":
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language,
        )
    else:
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

    return {"translated_text": response["TranslatedText"], "source_language": response["SourceLanguageCode"]}
