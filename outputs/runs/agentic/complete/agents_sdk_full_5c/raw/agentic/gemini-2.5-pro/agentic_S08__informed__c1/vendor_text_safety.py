import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_vendor_text(text_to_moderate: str) -> dict:
    """
    Moderates vendor-provided text fields for harmful content using
    Azure AI Content Safety.
    """
    if not text_to_moderate:
        return {"is_safe": True, "details": {}}

    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(text=text_to_moderate, categories=[
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ])
    
    try:
        response = client.analyze_text(request)
    except Exception as e:
        print(f"Error during content safety analysis: {e}")
        # Fail safe: if the service fails, assume content is unsafe.
        return {"is_safe": False, "error": str(e)}

    results = {}
    is_safe = True
    for category in response.categories_analysis:
        results[category.category.value] = category.severity
        if category.severity > 0:
            is_safe = False

    return {"is_safe": is_safe, "details": results}
