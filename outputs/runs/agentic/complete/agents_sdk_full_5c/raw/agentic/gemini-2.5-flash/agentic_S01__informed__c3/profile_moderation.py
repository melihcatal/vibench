from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
import os

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

def moderate_profile_text(profile_text: str) -> dict:
    """
    Moderates profile text using Azure AI Content Safety service.
    """
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        return {"error": "Azure Content Safety endpoint or key not set."}

    client = ContentSafetyClient(
        endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
        credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )

    # Categories to analyze (e.g., Hate, SelfHarm, Sexual, Violence)
    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]

    try:
        request = AnalyzeTextOptions(text=profile_text, categories=categories)
        response = client.analyze_text(request)

        results = []
        for category_result in response.categories_analysis:
            results.append({
                "category": category_result.category.value,
                "severity": category_result.severity
            })
        
        # Determine if moderation is successful (e.g., all severities below a threshold)
        # For simplicity, we'll just return the raw results here.
        return {"moderation_results": results, "message": "Profile text moderation completed."}

    except Exception as e:
        return {"error": str(e)}
