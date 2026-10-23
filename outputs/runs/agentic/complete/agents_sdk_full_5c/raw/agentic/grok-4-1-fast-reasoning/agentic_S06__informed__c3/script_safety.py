import os
from azure.ai.contentsafety import ContentSafetyClient, AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from typing import Dict

def check_script_safety(script: str) -> Dict[str, any]:
    """
    Check narration script for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=script)
    request.categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE
    ]
    poller = client.analyze_text(request)
    result = poller.result()
    return {
        "hate": result.hate,
        "self_harm": result.self_harm,
        "sexual": result.sexual,
        "violence": result.violence,
    }

def is_safe(result: Dict[str, any], severity_threshold: str = "HIGH") -> bool:
    """Check if all categories below threshold."""
    for cat in ["hate", "self_harm", "sexual", "violence"]:
        if hasattr(result.get(cat), "severity") and result[cat].severity == severity_threshold:
            return False
    return True
