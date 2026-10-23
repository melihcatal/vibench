import boto3


def log_message_translate(payload, config=None):
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload.get("source_language", "en"),
        TargetLanguageCode=payload["target_language"],
    )
    return {"translated_text": response.get("TranslatedText"), "target_language": payload["target_language"]}
