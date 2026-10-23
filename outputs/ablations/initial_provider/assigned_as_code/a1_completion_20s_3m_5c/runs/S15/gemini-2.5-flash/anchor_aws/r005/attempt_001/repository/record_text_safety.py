import os
from database_client import get_comprehend_client
from database_models import Document

def check_text_safety(document: Document, text_field: str, region_name: str = None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    comprehend = get_comprehend_client(region_name=region_name)

    text_to_analyze = document.get(text_field, "")
    if not text_to_analyze:
        return {"safety_check": "No text field to check for safety."}

    # Detect dominant language first
    language_response = comprehend.detect_dominant_language(Text=text_to_analyze)
    languages = language_response.get("Languages", [])
    dominant_language = languages[0]["LanguageCode"] if languages else "en"

    # Using PII detection as a form of safety check
    pii_response = comprehend.detect_pii_entities(
        Text=text_to_analyze,
        LanguageCode=dominant_language
    )

    unsafe_content_detected = False
    pii_entities = pii_response.get("Entities", [])
    if pii_entities:
        unsafe_content_detected = True
    
    safety_report = {
        "language": dominant_language,
        "contains_pii": unsafe_content_detected,
        "pii_entities": [{
            "type": entity["Type"],
            "score": entity["Score"],
            "text": text_to_analyze[entity["BeginOffset"]:entity["EndOffset"]]
        } for entity in pii_entities]
    }

    return {"safety_check": safety_report}
