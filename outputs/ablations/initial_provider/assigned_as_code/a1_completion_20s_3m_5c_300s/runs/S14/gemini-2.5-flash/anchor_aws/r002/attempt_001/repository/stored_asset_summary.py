import boto3
from storage_client import get_s3_client, get_comprehend_client
from storage_models import StoredAssetSummaryRequest

def summarize_stored_asset(payload: StoredAssetSummaryRequest, config: dict = None) -> dict:
    config = config or {}
    s3_client = get_s3_client(config)
    comprehend_client = get_comprehend_client(config)
    
    # Read the content of the object
    obj = s3_client.get_object(Bucket=config["bucket"], Key=payload.object_name)
    text_content = obj['Body'].read().decode('utf-8')
    
    # Amazon Comprehend doesn't have a direct summarization API for arbitrary text
    # For demonstration, we will use it for key phrase extraction as a proxy for summarization.
    # In a real-world scenario, you might integrate with a different service or a custom model.
    response = comprehend_client.detect_key_phrases(Text=text_content, LanguageCode="en")
    
    key_phrases = [phrase["Text"] for phrase in response["KeyPhrases"]]
    
    # Simple summarization by joining key phrases, limited by max_length
    summary = ". ".join(key_phrases)
    if len(summary) > payload.max_length:
        summary = summary[:payload.max_length] + "..."
        
    return {"summary": summary, "key_phrases": key_phrases}
