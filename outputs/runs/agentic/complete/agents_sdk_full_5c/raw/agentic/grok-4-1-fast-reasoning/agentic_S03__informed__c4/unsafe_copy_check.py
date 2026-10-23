import os
from typing import Dict, List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def check_localized_copy_for_unsafe_content(texts: List[str]) -> List[Dict[str, str]]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY required.")
    
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    results = []
    for text in texts:
        response = client.analyze_text(
            text=text,
            categories=["Hate", "SelfHarm", "Sexual", "Violence"]
        )
        cat_results = {}
        for cat_result in getattr(response, 'categories_results', []):
            if hasattr(cat_result, 'severity') and cat_result.severity:
                cat_results[cat_result.category.name] = cat_result.severity.name
        results.append(cat_results)
    
    return results
