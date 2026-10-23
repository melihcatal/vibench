from typing import Dict, Any
from model_models import ChatResponse
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os


def check_platform_output_safety(response: ChatResponse) -> Dict[str, Any]:
    """
    Checks Azure AI Inference model output for unsafe content using Azure Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not all([endpoint, key]):
        raise ValueError("Missing required Azure Content Safety configuration.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    text = response.content

    request = AnalyzeTextOptions(text=text)
    result = client.analyze_text(request)

    return {
        "is_safe": all(
            category.severity <= 2 for category in result.categories_analysis
        ),
        "categories": {
            category.category.name: category.severity
            for category in result.categories_analysis
        },
        "raw_result": result,
    }
