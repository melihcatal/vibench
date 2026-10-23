import boto3


def stored_text_translate(payload, config=None):
    translate = boto3.client("translate", region_name=(config or {}).get("region"))
    return translate.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload.get("source_language", "auto"),
        TargetLanguageCode=payload["target_language"],
    )
