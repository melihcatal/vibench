import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

def record_text_safety(text_content: str) -> dict:
    """
    Check user-generated document fields for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_content)

    # You can also add categories to be analyzed or blocklist names.
    # request = AnalyzeTextOptions(text=text_content, categories=[TextCategory.HATE, TextCategory.SELF_HARM])

    response = client.analyze_text(request)

    # Convert response to a dictionary for easier consumption
    result = {
        "hate": response.hate.severity,
        "self_harm": response.self_harm.severity,
        "sexual": response.sexual.severity,
        "violence": response.violence.severity,
    }

    return result
