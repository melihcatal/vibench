import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_profile_text(profile_text: str) -> bool:
    """
    Moderates user profile text using Azure Content Safety.
    Returns True if the text is safe, False otherwise.
    """
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=profile_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return False

    # Check for high severity content
    if (
        response.hate_result.severity > 1 or
        response.self_harm_result.severity > 1 or
        response.sexual_result.severity > 1 or
        response.violence_result.severity > 1
    ):
        return False

    return True
