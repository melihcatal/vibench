import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def safety_threshold(text: str, category_thresholds: dict):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(text=text, categories=[
        TextCategory.VIOLENCE,
        TextCategory.HATE_SPEECH,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM
    ], output_type="FourPoint")

    response = client.analyze_text(request)

    allowed = True
    decisions = {}

    for category in response.categories_analysis:
        category_name = category.category.value
        severity = category.severity
        
        threshold = category_thresholds.get(category_name, 0) # Default to 0 if no threshold defined
        
        if severity >= threshold and threshold > 0: # Only disallow if a threshold is set and exceeded
            allowed = False
            decisions[category_name] = f"Disallowed: Severity {severity} exceeds threshold {threshold}"
        else:
            decisions[category_name] = f"Allowed: Severity {severity} within threshold {threshold}"
            
    return {"allowed": allowed, "decisions": decisions}
