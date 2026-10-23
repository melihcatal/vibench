import boto3


def compliance_note_translate(payload, config=None):
    config = config or {}
    translate = boto3.client("translate", region_name=config.get("region"))
    response = translate.translate_text(
        Text=payload.get("text", ""),
        SourceLanguageCode=payload.get("source_language", "auto"),
        TargetLanguageCode=payload.get("target_language", "en"),
    )
    return {"translated_text": response["TranslatedText"], "source_language": response.get("SourceLanguageCode")}
