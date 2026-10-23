import os
from typing import Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def vendor_text_safety(vendor_text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=vendor_text)
    request.categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]
    poller = client.begin_analyze_text(request)
    result = poller.result()
    severity = {
        "hate": result.hate_result.severity.value if result.hate_result else None,
        "sexual": result.sexual_result.severity.value if result.sexual_result else None,
        "violence": result.violence_result.severity.value
        if result.violence_result
        else None,
        "self_harm": result.self_harm_result.severity.value
        if result.self_harm_result
        else None,
    }
    blocked = any(
        getattr(result, cat.name.lower() + "_result").blocked
        for cat in request.categories
        if hasattr(result, cat.name.lower() + "_result")
    )
    return {"severities": severity, "blocked": blocked}
