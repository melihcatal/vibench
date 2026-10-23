import os
from typing import Dict, Any, List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_text_safety(document: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Checks user-generated document fields for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    results = []
    
    for field, value in document.items():
        if isinstance(value, str) and len(value) > 0:
            options = AnalyzeTextOptions(text=value)
            response = client.analyze_text(options)
            
            for result in response.categories_analysis:
                if result.severity > 0:
                    results.append({
                        "field": field,
                        "category": result.category,
                        "severity": result.severity
                    })
    
    return results