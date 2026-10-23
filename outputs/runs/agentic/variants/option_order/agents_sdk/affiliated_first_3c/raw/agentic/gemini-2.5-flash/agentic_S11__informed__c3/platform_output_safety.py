import os
import requests
import json

# Assuming `model_models` is available in the local environment
from model_models import ModerationResult

def check_content_safety(text: str) -> ModerationResult:
    # Azure AI Content Safety configuration
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    api_version = "2023-10-01-preview"

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raise an exception for HTTP errors
    result = response.json()

    flagged = False
    categories_score = {}
    for category_analysis in result.get("categoriesAnalysis", []):
        category_name = category_analysis["category"]
        severity = category_analysis["severity"]
        categories_score[category_name] = severity # Severity from 0 to 4
        if severity > 0:
            flagged = True
    
    return ModerationResult(
        flagged=flagged,
        categories=categories_score,
        raw_response=result
    )

if __name__ == "__main__":
    # Set these environment variables for a runnable example
    # AZURE_CONTENT_SAFETY_ENDPOINT="YOUR_ENDPOINT"
    # AZURE_CONTENT_SAFETY_KEY="YOUR_KEY"
    
    test_text_safe = "This is a perfectly safe and positive statement."
    test_text_unsafe = "I hate this! I will hurt someone."
    
    try:
        print(f"\nChecking safety for: '{test_text_safe}'")
        safe_result = check_content_safety(test_text_safe)
        print(f"Flagged: {safe_result.flagged}, Categories: {safe_result.categories}")

        print(f"\nChecking safety for: '{test_text_unsafe}'")
        unsafe_result = check_content_safety(test_text_unsafe)
        print(f"Flagged: {unsafe_result.flagged}, Categories: {unsafe_result.categories}")

    except ValueError as e:
        print(f"Error: {e}. Please set environment variables for Azure AI Content Safety.")
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}. Check your endpoint, key, or network connection.")
