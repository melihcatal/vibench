import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_log_content_safety(log_message: str) -> dict:
    """
    Checks log message text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

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
        print(f"Analyze text failed: {e.response.text}")
        return {}

    return {
        "Hate": response.hate_result.severity,
        "SelfHarm": response.self_harm_result.severity,
        "Sexual": response.sexual_result.severity,
        "Violence": response.violence_result.severity,
    }


if __name__ == "__main__":
    unsafe_message = (
        "This is a terrible and violent message that should not be in logs."
    )
    safe_message = "User successfully updated their profile."

    try:
        print(f"Checking unsafe message: '{unsafe_message}'")
        safety_result_unsafe = check_log_content_safety(unsafe_message)
        print(safety_result_unsafe)

        print(f"\nChecking safe message: '{safe_message}'")
        safety_result_safe = check_log_content_safety(safe_message)
        print(safety_result_safe)

    except ValueError as e:
        print(e)
