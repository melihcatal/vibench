import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from observability_models import TextSafetyRequest, TextSafetyResponse

def check_log_text_safety(request: TextSafetyRequest, config: Dict[str, Any] = None) -> TextSafetyResponse:
    config = config or {}

    content_safety_endpoint = config.get('AZURE_CONTENT_SAFETY_ENDPOINT', os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT'))
    content_safety_key = config.get('AZURE_CONTENT_SAFETY_KEY', os.environ.get('AZURE_CONTENT_SAFETY_KEY'))

    if not all([content_safety_endpoint, content_safety_key]):
        raise ValueError("Azure Content Safety endpoint or key not configured.")

    client = ContentSafetyClient(content_safety_endpoint, AzureKeyCredential(content_safety_key))

    # Example categories for analysis, adjust as needed
    request_options = AnalyzeTextOptions(text=request.text, categories=[
        TextCategory.VIOLENCE,
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL
    ])

    response = client.analyze_text(request_options)

    is_safe = True
    reasons = []

    if response.hate_result and response.hate_result.severity > 0:
        is_safe = False
        reasons.append(f"Hate content detected with severity {response.hate_result.severity}.")
    if response.sexual_result and response.sexual_result.severity > 0:
        is_safe = False
        reasons.append(f"Sexual content detected with severity {response.sexual_result.severity}.")
    if response.self_harm_result and response.self_harm_result.severity > 0:
        is_safe = False
        reasons.append(f"Self-harm content detected with severity {response.self_harm_result.severity}.")
    if response.violence_result and response.violence_result.severity > 0:
        is_safe = False
        reasons.append(f"Violence content detected with severity {response.violence_result.severity}.")
    
    return TextSafetyResponse(is_safe=is_safe, reasons=reasons)
