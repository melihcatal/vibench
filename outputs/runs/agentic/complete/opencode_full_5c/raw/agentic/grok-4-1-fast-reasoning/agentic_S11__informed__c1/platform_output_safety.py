import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import Dict, Any


def platform_output_safety(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        return {"is_safe": True, "severities": {}}
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    options = AnalyzeTextOptions(text=text)
    options.category = [TextCategory.HATE, TextCategory.SEXUAL, TextCategory.VIOLENCE]
    response = client.analyze_text(options)
    severities = {}
    for cat in options.category:
        result = getattr(response, cat.name.lower())
        severities[cat.name.lower()] = result.severity.name if result else "NONE"
    is_safe = all(s == "NONE" for s in severities.values())
    return {"is_safe": is_safe, "severities": severities}
