import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_annotation_safety(annotation_text: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Azure AI Content Safety.

    :param annotation_text: The text to analyze.
    :return: A dictionary with the analysis results.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=annotation_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e.message}"}

    results = {
        "hate": TextCategory.HATE,
        "self_harm": TextCategory.SELF_HARM,
        "sexual": TextCategory.SEXUAL,
        "violence": TextCategory.VIOLENCE,
    }
    
    is_unsafe = False
    analysis = {}
    for category, category_name in results.items():
        result = next((r for r in response.categories_analysis if r.category == category_name), None)
        if result:
            analysis[category] = {"severity": result.severity}
            if result.severity > 0:
                is_unsafe = True

    return {"is_unsafe": is_unsafe, "analysis": analysis}
