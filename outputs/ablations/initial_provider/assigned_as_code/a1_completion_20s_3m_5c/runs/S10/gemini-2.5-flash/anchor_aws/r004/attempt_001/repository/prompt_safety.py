from model_client import BedrockModelClient
from model_models import TextPayload

def prompt_safety_check(payload: TextPayload, config=None):
    client = BedrockModelClient(region_name=config.get("region") if config else None)

    # Using Amazon Comprehend for PII detection as a safety check example
    # Note: A comprehensive safety check might involve multiple services or a dedicated moderation model.
    entities = client.detect_pii(text=payload.text)
    
    unsafe_content_detected = False
    detected_types = set()
    if entities:
        unsafe_content_detected = True
        for entity in entities:
            detected_types.add(entity['Type'])

    return {
        "is_safe": not unsafe_content_detected,
        "detected_pii_types": list(detected_types),
        "full_detection_response": entities
    }
