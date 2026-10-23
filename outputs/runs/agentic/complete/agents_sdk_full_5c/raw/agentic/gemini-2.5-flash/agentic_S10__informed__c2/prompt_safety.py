import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from model_models import SafetyCheckRequest, SafetyCheckResponse

def check_prompt_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """Checks prompts and generated text for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    text_categories = []
    for category_str in request.categories:
        try:
            text_categories.append(TextCategory(category_str))
        except ValueError:
            print(f"Warning: Invalid category '{category_str}' ignored.")

    request_body = AnalyzeTextOptions(text=request.text_content, categories=text_categories)

    # Provider SDK import: azure.ai.contentsafety
    # Provider API hostname: Implicitly from endpoint
    # Provider-specific client class: ContentSafetyClient

    response = client.analyze_text(request_body)

    is_safe = True
    moderation_results = {}
    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            moderation_results[category_analysis.category.name] = {
                "severity": category_analysis.severity,
                "is_detected": category_analysis.severity > 0
            }
            if category_analysis.severity > 0:
                is_safe = False

    return SafetyCheckResponse(is_safe=is_safe, moderation_results=moderation_results)
