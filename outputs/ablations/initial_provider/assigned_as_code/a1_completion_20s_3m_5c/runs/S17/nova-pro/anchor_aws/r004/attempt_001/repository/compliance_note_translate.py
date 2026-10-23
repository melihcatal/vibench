import boto3


def compliance_note_translate(note, target_language, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(Text=note, SourceLanguageCode="en", TargetLanguageCode=target_language)
    return {"translated_note": response["TranslatedText"]}