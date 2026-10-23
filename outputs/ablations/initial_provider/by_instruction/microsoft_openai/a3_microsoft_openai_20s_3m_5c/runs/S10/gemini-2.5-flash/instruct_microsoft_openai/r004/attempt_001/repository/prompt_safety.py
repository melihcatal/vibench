import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_safety(text: str) -> dict:
    """
    Checks prompts and generated text for unsafe content using Azure Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    # Example: enable all text categories
    request.categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
        TextCategory.VIOLENCE,
    ]

    response = client.analyze_text(request)

    result = {}
    if response.hate_result:
        result["hate"] = {"severity": response.hate_result.severity}
    if response.sexual_result:
        result["sexual"] = {"severity": response.sexual_result.severity}
    if response.self_harm_result:
        result["self_harm"] = {"severity": response.self_harm_result.severity}
    if response.violence_result:
        result["violence"] = {"severity": response.violence_result.severity}
    
    return result