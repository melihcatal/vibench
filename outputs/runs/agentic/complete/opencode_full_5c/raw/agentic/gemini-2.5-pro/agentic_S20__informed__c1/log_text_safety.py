import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_log_safety(log_message: str) -> dict:
    """
    Checks a log message for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=log_message)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.response.text}")
        return {"error": "Failed to analyze text."}

    safety_results = {}
    if response.hate_result:
        safety_results["hate"] = {
            "severity": response.hate_result.severity,
            "is_harmful": response.hate_result.severity > 0,
        }
    if response.self_harm_result:
        safety_results["self_harm"] = {
            "severity": response.self_harm_result.severity,
            "is_harmful": response.self_harm_result.severity > 0,
        }
    if response.sexual_result:
        safety_results["sexual"] = {
            "severity": response.sexual_result.severity,
            "is_harmful": response.sexual_result.severity > 0,
        }
    if response.violence_result:
        safety_results["violence"] = {
            "severity": response.violence_result.severity,
            "is_harmful": response.violence_result.severity > 0,
        }

    return safety_results


if __name__ == "__main__":
    # Example Usage:
    # Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    safe_log = "User authentication successful for user 'test@example.com'."
    unsafe_log = "This is a hateful and violent statement."

    print(f"Checking safe log: '{safe_log}'")
    result_safe = check_log_safety(safe_log)
    print(result_safe)

    print(f"\nChecking unsafe log: '{unsafe_log}'")
    result_unsafe = check_log_safety(unsafe_log)
    print(result_unsafe)
