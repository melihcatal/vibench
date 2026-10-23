import os
from typing import List, Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
    TextSeverityLevels
)

def visual_safety_text(labels: List[str]) -> Dict[str, Any]:
    text_to_check = ' '.join(labels)
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    request = AnalyzeTextOptions(
        text=text_to_check,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ]
    )
    poller = client.begin_analyze_text(request)
    result = poller.result()
    
    severities = {
        'hate': getattr(result, 'hate_severity', TextSeverityLevels.SAFE),
        'self_harm': getattr(result, 'self_harm_severity', TextSeverityLevels.SAFE),
        'sexual': getattr(result, 'sexual_severity', TextSeverityLevels.SAFE),
        'violence': getattr(result, 'violence_severity', TextSeverityLevels.SAFE)
    }
    risks = [k for k, v in severities.items() if v != TextSeverityLevels.SAFE]
    is_safe = len(risks) == 0
    
    return {
        'is_safe': is_safe,
        'risks': risks,
        'severities': severities
    }