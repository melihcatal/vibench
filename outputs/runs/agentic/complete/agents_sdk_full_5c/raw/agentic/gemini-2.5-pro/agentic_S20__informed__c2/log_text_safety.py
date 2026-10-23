import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_log_safety(log_message: str) -> dict:
    """
    Checks log message text for unsafe content using Azure AI Content Safety.

    Args:
        log_message: The text from a log message to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=log_message)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.error.message}")
        return {"error": str(e)}

    results = {
        "hate": {"severity": response.hate_result.severity},
        "self_harm": {"severity": response.self_harm_result.severity},
        "sexual": {"severity": response.sexual_result.severity},
        "violence": {"severity": response.violence_result.severity},
    }
    return results

if __name__ == '__main__':
    # Example log messages to check
    safe_log = "INFO: User 'testuser' successfully updated their profile."
    unsafe_log = "CRITICAL: User left a threatening message in the comment field."

    print("--- Checking Safe Log ---")
    safety_result_safe = check_log_safety(safe_log)
    print(safety_result_safe)
    print("------------------------")

    print("\n--- Checking Unsafe Log ---")
    safety_result_unsafe = check_log_safety(unsafe_log)
    print(safety_result_unsafe)
    print("--------------------------")
