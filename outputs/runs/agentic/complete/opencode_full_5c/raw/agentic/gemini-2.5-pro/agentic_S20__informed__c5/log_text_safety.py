import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_log_safety(log_message: str) -> dict:
    """
    Checks a log message for unsafe content using Azure AI Content Safety.

    Args:
        log_message: The text of the log message to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise EnvironmentError("Azure Content Safety credentials are not set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=log_message,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.response.json()}")
        return {}

    return {
        "hate_result": response.hate_result.severity if response.hate_result else 0,
        "self_harm_result": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_result": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_result": response.violence_result.severity
        if response.violence_result
        else 0,
    }


if __name__ == "__main__":
    safe_message = "Application started successfully on port 8080."
    unsafe_message = (
        "User uploaded a hateful and violent comment."  # Example of unsafe content
    )

    print(f"Analyzing safe message: '{safe_message}'")
    safe_result = check_log_safety(safe_message)
    print(safe_result)

    print(f"\nAnalyzing unsafe message: '{unsafe_message}'")
    unsafe_result = check_log_safety(unsafe_message)
    print(unsafe_result)
