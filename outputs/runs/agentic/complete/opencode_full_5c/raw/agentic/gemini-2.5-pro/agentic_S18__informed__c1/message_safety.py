import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_message_safety(text_to_analyze: str) -> bool:
    """
    Checks message payload text for unsafe content using Azure AI Content Safety.
    Returns True if the content is safe, False otherwise.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_analyze, categories=[TextCategory.HATE])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return False

    # A hate category severity > 0 is considered unsafe.
    if response.hate_result:
        print(f"Hate severity: {response.hate_result.severity}")
        if response.hate_result.severity > 0:
            return False

    return True


if __name__ == "__main__":
    safe_text = "This is a friendly message about a product update."
    unsafe_text = "This message contains hateful and offensive speech."

    is_safe = check_message_safety(safe_text)
    print(f"'{safe_text}' is safe: {is_safe}")

    is_safe = check_message_safety(unsafe_text)
    print(f"'{unsafe_text}' is safe: {is_safe}")
