import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions


def check_log_safety(log_message: str) -> dict:
    """
    Checks a log message for unsafe content using Azure AI Content Safety.

    Args:
        log_message: The text of the log message to analyze.

    Returns:
        A dictionary with the analysis results.
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
    except Exception as e:
        return {"error": str(e)}

    result = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity
        if response.violence_result
        else 0,
    }
    return result


if __name__ == "__main__":
    if os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT") and os.environ.get(
        "AZURE_CONTENT_SAFETY_KEY"
    ):
        safe_message = "User authentication successful for user_id: 12345"
        unsafe_message = "User profile updated with violent and hateful content."

        print(f"Analyzing safe message: '{safe_message}'")
        safe_result = check_log_safety(safe_message)
        print(safe_result)

        print(f"\nAnalyzing unsafe message: '{unsafe_message}'")
        unsafe_result = check_log_safety(unsafe_message)
        print(unsafe_result)
    else:
        print(
            "AZURE_CONTENT_SAFETY_ENDPOINT and/or AZURE_CONTENT_SAFETY_KEY not set. Skipping example run."
        )
