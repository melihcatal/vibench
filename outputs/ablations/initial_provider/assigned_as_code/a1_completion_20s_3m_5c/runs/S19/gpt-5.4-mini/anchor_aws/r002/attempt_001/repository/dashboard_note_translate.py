import boto3


def dashboard_note_translate(payload, config=None):
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload.get("source_language", "auto"),
        TargetLanguageCode=payload["target_language"],
    )
    return {"text": response["TranslatedText"], "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode")}
