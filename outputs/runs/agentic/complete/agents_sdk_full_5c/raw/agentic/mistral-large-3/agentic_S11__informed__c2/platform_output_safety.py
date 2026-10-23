import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
)
from model_models import SafetyCheckRequest, SafetyCheckResponse


def check_output_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """Check model output for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    analysis_request = AnalyzeTextOptions(
        text=request.text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )
    
    response = client.analyze_text(analysis_request)
    
    violations = {
        "hate": response.hate_result.severity if response.hate_result else 0,
        "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual": response.sexual_result.severity if response.sexual_result else 0,
        "violence": response.violence_result.severity if response.violence_result else 0,
    }
    
    is_safe = all(severity == 0 for severity in violations.values())
    
    return SafetyCheckResponse(
        is_safe=is_safe,
        violations=violations,
    )