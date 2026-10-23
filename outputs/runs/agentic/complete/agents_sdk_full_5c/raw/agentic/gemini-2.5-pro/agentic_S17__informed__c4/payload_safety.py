"""
Checks a decrypted text payload for unsafe content using Azure AI Content Safety.
"""
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_payload_safety(text_payload: str) -> dict:
    """
    Analyzes a text payload for harmful content using Azure AI Content Safety.

    Args:
        text_payload: The string to analyze.

    Returns:
        A dictionary summarizing the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_payload)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.error.message}")
        return {"error": str(e)}

    results = {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
        "violence_severity": response.violence_result.severity if response.violence_result else 0,
    }
    
    # A simple determination of safety
    is_safe = all(severity < 2 for severity in results.values())
    results["is_safe"] = is_safe

    return results

# Example Usage (for demonstration if run directly)
if __name__ == '__main__':
    safe_text = "This is a perfectly normal and safe sentence."
    unsafe_text = "This text contains hateful and violent content that should be flagged."

    if os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"):
        print(f"Checking safe text: '{safe_text}'")
        safety_report_safe = check_payload_safety(safe_text)
        print(safety_report_safe)

        print(f"\nChecking unsafe text: '{unsafe_text}'")
        safety_report_unsafe = check_payload_safety(unsafe_text)
        print(safety_report_unsafe)
    else:
        print("Skipping example: AZURE_CONTENT_SAFETY_ENDPOINT environment variable not set.")
