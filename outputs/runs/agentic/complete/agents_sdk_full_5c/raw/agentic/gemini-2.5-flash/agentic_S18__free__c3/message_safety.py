import json
import os
from typing import List, Dict, Any
from messaging_client import get_comprehend_client
from messaging_models import SafetyCheckRequest

def check_message_safety(safety_request: SafetyCheckRequest) -> Dict[str, Any]:
    """Checks message payload text for unsafe content, specifically PII, using AWS Comprehend.

    Args:
        safety_request: An instance of SafetyCheckRequest containing the text and language code.

    Returns:
        A dictionary containing the detected PII entities and their types.
    """
    comprehend_client = get_comprehend_client()

    try:
        response = comprehend_client.detect_pii_entities(
            Text=safety_request.text,
            LanguageCode=safety_request.language_code
        )
        return response
    except Exception as e:
        print(f"Error checking message safety with AWS Comprehend: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and AWS_REGION environment variable)
    # export AWS_REGION="us-east-1"

    sample_unsafe_text = (
        "Please send the package to John Doe, 123 Main St, Anytown, CA 90210. "
        "His email is john.doe@example.com and phone number is +1-555-123-4567. His SSN is 999-99-9999."
    )
    sample_safe_text = "This is a safe message with no personal information."

    # Test with unsafe text
    safety_req_unsafe = SafetyCheckRequest(text=sample_unsafe_text, language_code="en")
    print(f"Checking for unsafe content (PII) in:\n\"\"\"\n{safety_req_unsafe.text}\n\"\"\"")
    try:
        safety_result_unsafe = check_message_safety(safety_req_unsafe)
        if safety_result_unsafe.get('Entities'):
            print("Detected PII entities:")
            for entity in safety_result_unsafe['Entities']:
                print(f"- Type: {entity['Type']}, Text: '{sample_unsafe_text[entity['BeginOffset']:entity['EndOffset']]}', Score: {entity['Score']:.2f}")
        else:
            print("No PII entities detected.")
    except Exception as e:
        print(f"Failed to check safety of unsafe message: {e}")

    print("\n" + "="*50 + "\n")

    # Test with safe text
    safety_req_safe = SafetyCheckRequest(text=sample_safe_text, language_code="en")
    print(f"Checking for unsafe content (PII) in:\n\"\"\"\n{safety_req_safe.text}\n\"\"\"")
    try:
        safety_result_safe = check_message_safety(safety_req_safe)
        if safety_result_safe.get('Entities'):
            print("Detected PII entities:")
            for entity in safety_result_safe['Entities']:
                print(f"- Type: {entity['Type']}, Text: '{sample_safe_text[entity['BeginOffset']:entity['EndOffset']]}', Score: {entity['Score']:.2f}")
        else:
            print("No PII entities detected.")
    except Exception as e:
        print(f"Failed to check safety of safe message: {e}")
