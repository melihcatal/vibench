import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_text_safety(text_to_check: str) -> bool:
    """
    Checks if provided text contains any unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not configured.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_to_check,
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
        print(f"Analyze text failed: {e}")
        return False

    # A severity level > 0 indicates detected content
    if (
        response.hate_result
        and response.hate_result.severity > 0
        or response.self_harm_result
        and response.self_harm_result.severity > 0
        or response.sexual_result
        and response.sexual_result.severity > 0
        or response.violence_result
        and response.violence_result.severity > 0
    ):
        return False  # Unsafe

    return True  # Safe


if __name__ == "__main__":
    safe_label = "Standard database credentials for production."
    unsafe_note = "This is a terrible secret."

    is_safe = check_text_safety(safe_label)
    print(f"Label '{safe_label}' is safe: {is_safe}")

    is_safe = check_text_safety(unsafe_note)
    print(f"Note '{unsafe_note}' is safe: {is_safe}")
