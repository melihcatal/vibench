from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import os


def check_platform_output_safety(text: str, config: dict = None) -> dict:
    config = config or {}
    endpoint = config.get("AZURE_CONTENT_SAFETY_ENDPOINT") or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = config.get("AZURE_CONTENT_SAFETY_KEY") or os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key not found in config or environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
        # Process the response to determine if it's safe
        # This is a simplified example, real world would involve checking each category and its severity
        is_safe = True
        safety_results = {}
        if response.categories_analysis:
            for category_analysis in response.categories_analysis:
                safety_results[category_analysis.category.value] = {
                    "severity": category_analysis.severity,
                    "is_unsafe": category_analysis.severity > 0
                }
                if category_analysis.severity > 0:
                    is_safe = False
        
        return {"is_safe": is_safe, "analysis_results": safety_results}

    except Exception as e:
        return {"error": str(e), "is_safe": False}
