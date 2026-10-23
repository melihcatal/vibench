import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_text_safety(prompt: str):
    """
    Checks prompts for unsafe content using Azure AI Content Safety.
    """
    try:
        endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
        key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    except KeyError:
        return {"error": "Azure Content Safety credentials not set."}

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=prompt, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Azure API call failed: {e}"}

    return {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else 0,
        "violence_severity": response.violence_result.severity if response.violence_result else 0,
    }
