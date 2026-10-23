from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import os

def check_platform_output_safety(text_output, config=None):
    config = config or {}
    endpoint = config.get("azure_content_safety_endpoint", os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"))
    key = config.get("azure_content_safety_key", os.environ.get("AZURE_CONTENT_SAFETY_KEY"))

    if not endpoint or not key:
        print("Azure Content Safety endpoint or key not configured. Skipping safety check.")
        return {"is_safe": True, "analysis_results": []}

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Categories to check. Adjust as needed.
    categories = [
        TextCategory.HATE,
        TextCategory.VIOLENCE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ]

    request = AnalyzeTextOptions(text=text_output, categories=categories)
    response = client.analyze_text(request)

    analysis_results = []
    is_safe = True
    for category in response.categories_analysis:
        analysis_results.append({
            "category": category.category.value,
            "severity": category.severity
        })
        # Assuming severity 2 or higher indicates potential unsafety
        if category.severity and category.severity >= 2:
            is_safe = False
            
    return {"is_safe": is_safe, "analysis_results": analysis_results}
