import os
import boto3
from security_models import PayloadSafetyCheckRequest, PayloadSafetyCheckResponse, PIIEntity

def check_payload_safety(request: PayloadSafetyCheckRequest) -> PayloadSafetyCheckResponse:
    """
    Checks a decrypted text payload for unsafe content using AWS Comprehend (PII detection).
    """
    comprehend_client = boto3.client("comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    
    response = comprehend_client.detect_pii_entities(Text=request.payload, LanguageCode='en')
    
    unsafe_content_details = []
    for entity in response['Entities']:
        unsafe_content_details.append(PIIEntity(
            type=entity['Type'],
            score=entity['Score'],
            begin_offset=entity['BeginOffset'],
            end_offset=entity['EndOffset']
        ))
        
    has_unsafe_content = len(unsafe_content_details) > 0
    
    return PayloadSafetyCheckResponse(
        has_unsafe_content=has_unsafe_content,
        unsafe_content_details=unsafe_content_details
    )
