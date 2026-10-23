import boto3
from storage_client import get_s3_client, get_translate_client
from storage_models import StoredTextTranslateRequest

def translate_stored_text(payload: StoredTextTranslateRequest, config: dict = None) -> dict:
    config = config or {}
    s3_client = get_s3_client(config)
    translate_client = get_translate_client(config)
    
    # Read the content of the object
    obj = s3_client.get_object(Bucket=config["bucket"], Key=payload.object_name)
    text_content = obj['Body'].read().decode('utf-8')
    
    # Detect source language if not provided
    source_language = payload.source_language_code
    if not source_language:
        # In a real scenario, you might use Comprehend detect_dominant_language
        # For simplicity, we'll assume English if not specified.
        source_language = "en" # Placeholder
    
    response = translate_client.translate_text(
        Text=text_content,
        SourceLanguageCode=source_language,
        TargetLanguageCode=payload.target_language_code
    )
    
    return {"translated_text": response["TranslatedText"], "source_language": response["SourceLanguageCode"], "target_language": response["TargetLanguageCode"]}
