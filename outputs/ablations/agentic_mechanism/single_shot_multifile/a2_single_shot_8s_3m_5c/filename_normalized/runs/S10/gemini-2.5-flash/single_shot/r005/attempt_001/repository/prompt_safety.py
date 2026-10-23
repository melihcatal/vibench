import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE],
        blocklist_names=["MyBlocklist"] # Example blocklist, might not exist
    )

    try:
        response = client.analyze_text(request)
        results = {"categories_analysis": []}
        for category_analyzer_result in response.categories_analysis:
            results["categories_analysis"].append({
                "category": category_analyzer_result.category.value,
                "severity": category_analyzer_result.severity
            })
        return results
    except Exception as e:
        return {"error": str(e), "message": "Failed to analyze text for safety."}