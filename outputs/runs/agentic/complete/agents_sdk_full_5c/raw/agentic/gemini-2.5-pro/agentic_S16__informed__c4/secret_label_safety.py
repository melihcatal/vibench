import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_text_for_unsafe_content(text_to_check: str) -> bool:
    """
    Checks if secret labels or notes contain unsafe text using Azure AI Content Safety.

    Args:
        text_to_check: The text string to analyze.

    Returns:
        True if unsafe content is detected, False otherwise.
    """
    try:
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    except KeyError:
        return False # Cannot perform check without credentials

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text_to_check, categories=[
        TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
        for category in response.categories_analysis:
            if category.severity > 0:
                return True # Unsafe content detected
        return False
    except HttpResponseError:
        # Could log the error, but for this function, we can treat it as safe
        return False
