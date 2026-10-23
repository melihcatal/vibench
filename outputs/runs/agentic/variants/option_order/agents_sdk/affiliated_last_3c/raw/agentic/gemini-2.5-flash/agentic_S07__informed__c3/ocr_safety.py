import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextContentItem, TextCategory
from document_models import ContentSafetyResult

def check_ocr_text_safety(text_content: str) -> ContentSafetyResult:
    """
    Checks extracted document text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_content,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ],
        output_type="FourPoint" # Output scores in four-point scale (0-3)
    )

    response = client.analyze_text(request)

    safety_results = []
    if response.hate_result:
        safety_results.append({"category": "HATE", "severity": response.hate_result.severity})
    if response.self_harm_result:
        safety_results.append({"category": "SELF_HARM", "severity": response.self_harm_result.severity})
    if response.sexual_result:
        safety_results.append({"category": "SEXUAL", "severity": response.sexual_result.severity})
    if response.violence_result:
        safety_results.append({"category": "VIOLENCE", "severity": response.violence_result.severity})

    return ContentSafetyResult(text_safety_results=safety_results)
