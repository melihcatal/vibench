import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_text(text: str):
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

    results = {}
    for category in response.categories_analysis:
        results[category.category.value] = {
            "severity": category.severity
        }
    return results
