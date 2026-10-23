import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_log_content_safety(log_message: str) -> dict:
    """
    Checks a log message for unsafe content using Azure AI Content Safety.

    Args:
        log_message: The text content of the log to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=log_message)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.response.json()}")
        return {"error": str(e)}

    results = {}
    if response.hate_result:
        results['hate'] = {'severity': response.hate_result.severity}
    if response.self_harm_result:
        results['self_harm'] = {'severity': response.self_harm_result.severity}
    if response.sexual_result:
        results['sexual'] = {'severity': response.sexual_result.severity}
    if response.violence_result:
        results['violence'] = {'severity': response.violence_result.severity}
        
    return results

if __name__ == '__main__':
    # Example usage
    safe_log = "User authentication failed for user 'testuser'. Invalid credentials provided."
    unsafe_log = "The user entered a comment that threatens violence against our staff."

    print("--- Checking a safe log message ---")
    safe_results = check_log_content_safety(safe_log)
    print(safe_results)

    print("\n--- Checking an unsafe log message ---")
    unsafe_results = check_log_content_safety(unsafe_log)
    print(unsafe_results)

    # Example of a clearly unsafe message
    clearly_unsafe_log = "I'm going to find you and hurt you."
    print("\n--- Checking another unsafe log message ---")
    clearly_unsafe_results = check_log_content_safety(clearly_unsafe_log)
    print(clearly_unsafe_results)
