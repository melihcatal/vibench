
import os
from document_client import get_azure_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_content_safety(text: str) -> dict:
    client = get_azure_content_safety_client()

    # Construct request
    request = AnalyzeTextOptions(text=text)

    # Analyze text
    response = client.analyze_text(request)

    safety_results = {
        "hate": {"severity": response.hate_result.severity if response.hate_result else -1},
        "self_harm": {"severity": response.self_harm_result.severity if response.self_harm_result else -1},
        "sexual": {"severity": response.sexual_result.severity if response.sexual_result else -1},
        "violence": {"severity": response.violence_result.severity if response.violence_result else -1},
    }

    return safety_results
