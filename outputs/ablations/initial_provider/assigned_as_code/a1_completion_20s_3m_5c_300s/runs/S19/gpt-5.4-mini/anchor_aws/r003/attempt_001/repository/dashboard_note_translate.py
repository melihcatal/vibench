import boto3


def dashboard_note_translate(payload, config=None):
    translate = boto3.client("translate", region_name=(config or {}).get("region"))
    response = translate.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload.get("source_language", "auto"),
        TargetLanguageCode=payload["target_language"],
    )
    return {"text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode", payload.get("source_language", "auto")), "target_language": payload["target_language"]}
