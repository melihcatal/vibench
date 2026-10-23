import os
from typing import Dict, Any, List
from security_client import get_comprehend_client
from security_models import ModerationResult

def check_payload_safety(text: str, region: str = 'us-east-1') -> ModerationResult:
    """
    Checks decrypted text payloads for unsafe content using Amazon Comprehend Toxicity.
    """
    comprehend_client = get_comprehend_client(region)
    
    # Amazon Comprehend provides DetectToxicContent operation
    response = comprehend_client.detect_toxic_content(
        TextSegments=[{'Text': text}]
    )
    
    # Process the first segment's result (assuming single segment for simplicity)
    result = response['ResultList'][0]
    
    toxicity_score = result['Toxicity']
    
    # Define a simple threshold for 'unsafe' based on toxicity score.
    # This threshold might need tuning based on specific requirements.
    is_unsafe = toxicity_score > 0.7 
    
    categories = []
    for category in result.get('Labels', []):
        categories.append({
            "name": category['Name'],
            "score": category['Score']
        })

    return ModerationResult(
        input_text=text,
        toxicity_score=toxicity_score,
        is_unsafe=is_unsafe,
        categories=categories
    )

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    
    # example_text_safe = "This is a normal and friendly message."
    # example_text_unsafe = "I hate you, you are terrible!"
    
    # print("Checking safe text:")
    # safe_result = check_payload_safety(example_text_safe)
    # print(f"Text: '{safe_result.input_text}'")
    # print(f"Toxicity Score: {safe_result.toxicity_score}, Is Unsafe: {safe_result.is_unsafe}")
    # print(f"Categories: {safe_result.categories}")

    # print("\nChecking unsafe text:")
    # unsafe_result = check_payload_safety(example_text_unsafe)
    # print(f"Text: '{unsafe_result.input_text}'")
    # print(f"Toxicity Score: {unsafe_result.toxicity_score}, Is Unsafe: {unsafe_result.is_unsafe}")
    # print(f"Categories: {unsafe_result.categories}")
