import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_corpus_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not all([endpoint, key]):
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set for Azure Content Safety.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    
    response = client.analyze_text(request)

    safety_results = {
        "text": text,
        "hate_severity": 0,
        "self_harm_severity": 0,
        "sexual_severity": 0,
        "violence_severity": 0,
    }

    for category_result in response.categories_analysis:
        if category_result.category == TextCategory.HATE:
            safety_results["hate_severity"] = category_result.severity
        elif category_result.category == TextCategory.SELF_HARM:
            safety_results["self_harm_severity"] = category_result.severity
        elif category_result.category == TextCategory.SEXUAL:
            safety_results["sexual_severity"] = category_result.severity
        elif category_result.category == TextCategory.VIOLENCE:
            safety_results["violence_severity"] = category_result.severity
            
    return safety_results
