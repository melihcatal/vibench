import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def check_live_caption_safety(caption_text):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=caption_text)
    response = client.analyze_text(request)

    safety_results = {
        "hate": 0,
        "self_harm": 0,
        "sexual": 0,
        "violence": 0,
        "is_flagged": False
    }

    for category_assessment in response.categories_analysis:
        category_name = category_assessment.category.name.lower()
        safety_results[category_name] = category_assessment.severity
        if category_assessment.severity > 0:
            safety_results["is_flagged"] = True

    return safety_results