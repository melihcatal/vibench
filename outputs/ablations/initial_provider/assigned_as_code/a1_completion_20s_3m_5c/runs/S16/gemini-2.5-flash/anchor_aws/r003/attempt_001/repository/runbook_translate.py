import boto3


def runbook_translate(payload, config=None):
    config = config or {}
    translate_client = boto3.client("translate", region_name=config.get("region"))
    
    text_to_translate = payload["runbook_notes"]
    target_language_code = payload["target_language"]
    
    response = translate_client.translate_text(
        Text=text_to_translate,
        SourceLanguageCode="auto",  # Automatically detect source language
        TargetLanguageCode=target_language_code
    )
    
    translated_notes = response["TranslatedText"]
    source_language_code = response["SourceLanguageCode"]
    
    return {
        "secret_id": payload["secret_id"],
        "translated_notes": translated_notes,
        "source_language": source_language_code,
        "target_language": target_language_code,
    }
