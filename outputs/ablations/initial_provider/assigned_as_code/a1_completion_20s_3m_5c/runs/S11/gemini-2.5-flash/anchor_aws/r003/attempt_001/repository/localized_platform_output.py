import boto3

def localized_platform_output(text_output, target_language_code, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region", "us-east-1"))
    
    response = client.translate_text(
        Text=text_output,
        SourceLanguageCode="auto", # Automatically detect source language
        TargetLanguageCode=target_language_code
    )
    
    return {
        "translated_text": response["TranslatedText"],
        "source_language": response["SourceLanguageCode"],
        "target_language": target_language_code,
        "_original_response": response
    }
