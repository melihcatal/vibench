import boto3
import os
from security_client import get_comprehend_client

def check_payload_safety(text_payload: str, language_code: str = 'en') -> dict:
    """
    Checks a decrypted text payload for unsafe content using Amazon Comprehend Toxicity Detection.
    """
    comprehend_client = get_comprehend_client()
    
    try:
        response = comprehend_client.detect_toxic_content(
            Text=text_payload,
            LanguageCode=language_code
        )
        return response
    except Exception as e:
        print(f"Error checking payload safety with Amazon Comprehend: {e}")
        raise

if __name__ == '__main__':
    # Example Usage
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME must be set.
    
    example_safe_text = "This is a normal and safe message about software development."
    example_unsafe_text = "I hate this! You are so stupid and I will make you pay!"
    
    print("Checking safe text for toxicity:")
    try:
        safe_result = check_payload_safety(example_safe_text)
        print(f"Safe text analysis: {safe_result}")
    except Exception as e:
        print(f"Safety check failed for safe text: {e}")

    print("\nChecking unsafe text for toxicity:")
    try:
        unsafe_result = check_payload_safety(example_unsafe_text)
        print(f"Unsafe text analysis: {unsafe_result}")
    except Exception as e:
        print(f"Safety check failed for unsafe text: {e}")
