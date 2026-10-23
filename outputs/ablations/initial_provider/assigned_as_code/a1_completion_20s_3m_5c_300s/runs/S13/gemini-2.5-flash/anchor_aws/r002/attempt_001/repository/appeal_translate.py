import boto3
from typing import Dict, Any
from safety_client import get_aws_client

def appeal_translate(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_aws_client("translate", region_name=config.get("region", "us-east-1"))
    
    text_to_translate = payload["text"]
    source_language = payload.get("source_language", "auto") # Use 'auto' for automatic detection
    target_language = payload.get("target_language", "en")
    
    response = client.translate_text(
        Text=text_to_translate,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    
    translated_text = response["TranslatedText"]
    
    return {"translated_text": translated_text}
