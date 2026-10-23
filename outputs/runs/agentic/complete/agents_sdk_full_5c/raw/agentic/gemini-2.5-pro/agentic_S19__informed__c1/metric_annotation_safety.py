import os
from typing import Dict, Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_annotation_safety(annotation_text: str) -> Dict[str, Any]:
    """
    Checks free-text metric labels or annotations for unsafe text using
    Azure AI Content Safety.

    Args:
        annotation_text: The text to analyze.

    Returns:
        A dictionary containing the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=annotation_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP error during analysis: {e.message}"}

    results = {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
        "violence_severity": response.violence_result.severity if response.violence_result else 0,
    }
    
    # A simple pass/fail based on severity
    is_safe = all(severity == 0 for severity in results.values())
    results["is_safe"] = is_safe

    return results

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    safe_text = "This metric tracks the performance of the user profile update."
    unsafe_text = "This is a hateful comment." # Example of unsafe content

    print("Checking a safe annotation...")
    try:
        safe_result = check_annotation_safety(safe_text)
        print(f"Analysis for '{safe_text}': {safe_result}")
        assert safe_result.get("is_safe") is True
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("\nChecking an unsafe annotation...")
    try:
        unsafe_result = check_annotation_safety(unsafe_text)
        print(f"Analysis for '{unsafe_text}': {unsafe_result}")
        assert unsafe_result.get("is_safe") is False
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

