import boto3

def localized_platform_output(text: str, target_language_code: str, source_language_code: str = "en", config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    
    client = boto3.client("translate", region_name=region)
    
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    
    translated_text = response["TranslatedText"]
    
    return {"translated_text": translated_text, "source_language": source_language_code, "target_language": target_language_code}
