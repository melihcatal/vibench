import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from observability_models import SafetyCheckRequest

def log_text_safety(request: SafetyCheckRequest) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([endpoint, key]):
        raise ValueError("Missing Azure Content Safety environment variables: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # All categories will be analyzed. You can select specific categories if needed.
    request_body = AnalyzeTextOptions(text=request.text, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ])

    response = client.analyze_text(request_body)

    results = {"safety_scores": {}}
    for category_result in response.categories_analysis:
        results["safety_scores"][category_result.category.value] = category_result.severity

    return results
