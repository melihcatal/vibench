import boto3
import os
from typing import List, Dict, Any

def check_comprehend_safety(text: str) -> Dict[str, Any]:
    client = boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    # Example: Detect PII entities as a safety check
    # More comprehensive safety checks might involve custom classification models
    # or a combination of sentiment, key phrase, and entity detection.
    response = client.detect_pii_entities(
        Text=text,
        LanguageCode="en"
    )
    
    pii_entities = response.get("Entities", [])
    
    safety_report = {
        "unsafe_content_detected": bool(pii_entities),
        "pii_entities": pii_entities,
        # You could extend this with sentiment, toxicity scores if using other models
    }
    return safety_report

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_REGION="your-aws-region"
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # AWS_SECRET_ACCESS_KEY="your-secret-key"
    unsafe_text = "Please send the document to John Doe at john.doe@example.com."
    safe_text = "The quick brown fox jumps over the lazy dog."

    print("Checking unsafe text:")
    report_unsafe = check_comprehend_safety(unsafe_text)
    print(report_unsafe)

    print("\nChecking safe text:")
    report_safe = check_comprehend_safety(safe_text)
    print(report_safe)
