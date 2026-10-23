import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_visual_labels_safety(labels: list[str]) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    full_text_to_check = ", ".join(labels)

    analysis_options = AnalyzeTextOptions(text=full_text_to_check)

    response = client.analyze_text(analysis_options)

    safety_results = {}
    for category_result in response.categories_analysis:
        safety_results[category_result.category.value] = category_result.severity

    return safety_results
