import os
from typing import Dict, Any, List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeRequest, AnalyzeTextOptions


def check_text_safety(document: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    fields_text = " ".join(str(v) for v in document.get("fields", {}).values())
    
    request = TextAnalyzeRequest(
        text=fields_text,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        break_by_block=False
    )
    
    response = client.analyze_text(AnalyzeTextOptions(request))
    return {
        "is_safe": all(
            result.severity <= 2 for result in response.categories_analysis
        ),
        "results": [
            {
                "category": result.category,
                "severity": result.severity
            } for result in response.categories_analysis
        ]
    }