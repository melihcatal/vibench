import boto3

def check_payload_safety(text: str) -> dict:
    comprehend_client = boto3.client('comprehend')
    
    # Detect PII entities
    pii_response = comprehend_client.detect_pii_entities(Text=text, LanguageCode='en')
    pii_entities = pii_response['Entities']

    # Detect dominant language to ensure it's English for further analysis if needed
    # For simplicity, we are assuming English for PII detection above.
    # dominant_language_response = comprehend_client.detect_dominant_language(Text=text)
    # dominant_language = dominant_language_response['Languages'][0]['LanguageCode']

    # You can add more checks here like sentiment analysis, entity recognition for specific terms etc.

    is_safe = True
    unsafe_content_details = []

    if pii_entities:
        is_safe = False
        unsafe_content_details.append({
            "type": "PII_DETECTION",
            "details": pii_entities
        })

    return {
        "is_safe": is_safe,
        "unsafe_content_details": unsafe_content_details,
        "provider": "AWS Comprehend"
    }
