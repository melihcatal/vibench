from document_client import get_comprehend_client
from document_models import SafetyResult

def check_safety(text: str) -> SafetyResult:
    comprehend_client = get_comprehend_client()

    # Detect PII entities
    pii_response = comprehend_client.detect_pii_entities(Text=text, LanguageCode='en') # Assuming English for PII detection

    unsafe_content_detected = False
    details = {
        "pii_entities": pii_response['Entities']
    }

    if pii_response['Entities']:
        unsafe_content_detected = True

    # Add more safety checks as needed, e.g., custom entity recognition for specific keywords

    return SafetyResult(unsafe_content_detected=unsafe_content_detected, details=details)
