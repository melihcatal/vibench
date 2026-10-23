import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_log_text_safety(log_message: str) -> dict:
    """
    Checks log message text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=log_message)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e.message}"}

    results = {}
    if response.hate_result:
        results["hate"] = {"severity": response.hate_result.severity}
    if response.self_harm_result:
        results["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.sexual_result:
        results["sexual"] = {"severity": response.sexual_result.severity}
    if response.violence_result:
        results["violence"] = {"severity": response.violence_result.severity}

    return results


if __name__ == "__main__":
    # Example usage:
    unsafe_message = "This is a hateful and violent statement."
    safety_result = check_log_text_safety(unsafe_message)
    print(f"Safety analysis for '{unsafe_message}':")
    print(safety_result)

    safe_message = "User authentication successful."
    safety_result_safe = check_log_text_safety(safe_message)
    print(f"\nSafety analysis for '{safe_message}':")
    print(safety_result_safe)
