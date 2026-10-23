import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from model_models import SafetyCheckRequest

# Azure AI Content Safety service=Azure AI Content Safety; sdk=azure-ai-contentsafety; interface=sdk; auth=AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY


def check_safety(request: SafetyCheckRequest) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # By default, analyze all categories with default severities
    # You can customize categories and severities if needed
    analysis_options = AnalyzeTextOptions(text=request.text)

    try:
        response = client.analyze_text(analysis_options)
        results = {
            category.category.name: {
                "severity": category.severity,
                "detected": category.severity > 0,  # Severity > 0 indicates detection
            }
            for category in response.categories_analysis
        }
        return {"safety_analysis": results}
    except Exception as e:
        return {"error": str(e)}
