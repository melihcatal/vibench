import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory, SeverityType

def vendor_text_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    text_options = AnalyzeTextOptions(text=text)
    text_options.categories.append(TextCategory.HATE)
    text_options.categories.append(TextCategory.SEXUAL)
    text_options.categories.append(TextCategory.VIOLENCE)
    text_options.categories.append(TextCategory.SELF_HARM)
    
    poller = client.begin_analyze_text_content(text_options)
    result = poller.result()
    
    severity = {}
    for category in result.categories:
        if category.severity:
            severity[category.category.name] = category.severity.name
        else:
            severity[category.category.name] = "safe"
    
    return severity