from security_client import get_text_analytics_client
from azure.ai.textanalytics import PiiEntityDomain, PiiEntityCategory

def check_payload_safety(decrypted_text):
    text_analytics_client = get_text_analytics_client()

    documents = [decrypted_text]

    # Detect PII entities in the text
    # You can specify specific domains and categories if needed
    # For a comprehensive check, we use the default PII detection
    response = text_analytics_client.recognize_pii_entities(documents, domain=PiiEntityDomain.PHI)
    
    unsafe_content_found = False
    pii_entities = []

    for doc in response:
        if not doc.is_error:
            for entity in doc.entities:
                unsafe_content_found = True
                pii_entities.append({
                    'text': entity.text,
                    'category': entity.category.value,
                    'subcategory': entity.subcategory,
                    'offset': entity.offset,
                    'length': entity.length
                })
        else:
            # Handle error for this document
            print(f"Error: {doc.id} - {doc.error.code} - {doc.error.message}")

    return {
        'unsafe_content_found': unsafe_content_found,
        'pii_entities': pii_entities,
        'original_text_length': len(decrypted_text)
    }
