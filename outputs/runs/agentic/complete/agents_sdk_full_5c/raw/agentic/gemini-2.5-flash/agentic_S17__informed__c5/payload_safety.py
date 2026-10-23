import os
import requests
import json
from typing import Dict, Any
from security_models import ContentSafetyResult
from security_client import get_azure_content_safety_config

def check_payload_safety(text: str) -> ContentSafetyResult:
    """
    Checks a text payload for unsafe content using Azure AI Content Safety.

    Args:
        text: The text payload to check.

    Returns:
        A ContentSafetyResult object.
    """
    config = get_azure_content_safety_config()
    endpoint = config["endpoint"]
    key = config["key"]

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors

    result_json = response.json()
    
    # Determine if any category has a severity level that warrants blocking or review
    block_detected = False
    review_recommended = False
    for category_result in result_json.get("categoriesAnalysis", []):
        severity = category_result.get("severity", 0)
        # Assuming severity 2 or higher requires review, 4 requires blocking
        if severity >= 4:
            block_detected = True
            review_recommended = True
            break
        elif severity >= 2:
            review_recommended = True

    return ContentSafetyResult(
        text=text,
        categories_analysis=result_json.get("categoriesAnalysis", []),
        block_detected=block_detected,
        review_recommended=review_recommended
    )

if __name__ == '__main__':
    # Example usage (requires Azure AI Content Safety endpoint and key)
    # export AZURE_CONTENT_SAFETY_ENDPOINT="YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
    # export AZURE_CONTENT_SAFETY_KEY="YOUR_AZURE_CONTENT_SAFETY_KEY"

    # test_payload_1 = "I hate you, you are evil."
    # test_payload_2 = "This is a perfectly safe and positive message."
    # test_payload_3 = "Killing is wrong. I will hurt myself." # SelfHarm example

    # print(f"Checking payload: '{test_payload_1}'")
    # try:
    #     result = check_payload_safety(test_payload_1)
    #     print(f"  Block Detected: {result.block_detected}")
    #     print(f"  Review Recommended: {result.review_recommended}")
    #     for category in result.categories_analysis:
    #         print(f"    Category: {category['category']}, Severity: {category['severity']}")
    # except Exception as e:
    #     print(f"Error checking safety for '{test_payload_1}': {e}")
    # print("-" * 30)

    # print(f"Checking payload: '{test_payload_2}'")
    # try:
    #     result = check_payload_safety(test_payload_2)
    #     print(f"  Block Detected: {result.block_detected}")
    #     print(f"  Review Recommended: {result.review_recommended}")
    #     for category in result.categories_analysis:
    #         print(f"    Category: {category['category']}, Severity: {category['severity']}")
    # except Exception as e:
    #     print(f"Error checking safety for '{test_payload_2}': {e}")
    # print("-" * 30)
    
    # print(f"Checking payload: '{test_payload_3}'")
    # try:
    #     result = check_payload_safety(test_payload_3)
    #     print(f"  Block Detected: {result.block_detected}")
    #     print(f"  Review Recommended: {result.review_recommended}")
    #     for category in result.categories_analysis:
    #         print(f"    Category: {category['category']}, Severity: {category['severity']}")
    # except Exception as e:
    #     print(f"Error checking safety for '{test_payload_3}': {e}")
    # print("-" * 30)
