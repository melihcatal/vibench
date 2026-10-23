import boto3

def check_platform_output_safety(text_output, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    
    # Detect PII entities in the text output
    response = client.detect_pii_entities(Text=text_output, LanguageCode="en")
    
    # For simplicity, if any PII is detected, we'll flag it as unsafe.
    is_safe = not bool(response["Entities"])
    
    return {"is_safe": is_safe, "detected_pii_entities": response["Entities"], "_original_response": response}
