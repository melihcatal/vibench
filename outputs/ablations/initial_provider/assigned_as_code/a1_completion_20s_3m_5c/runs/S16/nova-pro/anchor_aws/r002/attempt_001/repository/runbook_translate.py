import boto3

def translate_runbook_notes(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    response = client.translate_text(Text=payload["notes"], SourceLanguageCode='en', TargetLanguageCode='es')
    return {"translated_notes": response["TranslatedText"]}