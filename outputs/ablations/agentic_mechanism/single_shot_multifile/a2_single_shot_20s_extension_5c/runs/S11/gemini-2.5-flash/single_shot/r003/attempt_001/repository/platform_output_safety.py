import os
from model_client import get_azure_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_content_safety(text_content: str) -> dict:
    client = get_azure_content_safety_client()
    
    request = AnalyzeTextOptions(text=text_content)

    response = client.analyze_text(request)
    
    safety_results = {
        "text": text_content,
        "hate_severity": response.hate_result.severity if response.hate_result else None,
        "self_harm_severity": response.self_harm_result.severity if response.self_harm_result else None,
        "sexual_severity": response.sexual_result.severity if response.sexual_result else None,
        "violence_severity": response.violence_result.severity if response.violence_result else None,
        "blocklist_matches": [m.blocklist_name for m in response.blocklist_matches] if response.blocklist_matches else []
    }
    return safety_results
