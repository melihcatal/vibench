import os
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_azure_content_safety_client
from safety_models import ModerationCategory, ModerationResult

def moderate_text(text: str) -> ModerationResult:
    client = get_azure_content_safety_client()
    request = AnalyzeTextOptions(text=text)
    
    response = client.analyze_text(request)

    categories = []
    overall_decision = "Safe"

    if response.hate_result:
        categories.append(ModerationCategory(category="Hate", severity=response.hate_result.severity, violates=response.hate_result.severity > 0))
        if response.hate_result.severity > 0:
            overall_decision = "Unsafe"
    if response.self_harm_result:
        categories.append(ModerationCategory(category="SelfHarm", severity=response.self_harm_result.severity, violates=response.self_harm_result.severity > 0))
        if response.self_harm_result.severity > 0:
            overall_decision = "Unsafe"
    if response.sexual_result:
        categories.append(ModerationCategory(category="Sexual", severity=response.sexual_result.severity, violates=response.sexual_result.severity > 0))
        if response.sexual_result.severity > 0:
            overall_decision = "Unsafe"
    if response.violence_result:
        categories.append(ModerationCategory(category="Violence", severity=response.violence_result.severity, violates=response.violence_result.severity > 0))
        if response.violence_result.severity > 0:
            overall_decision = "Unsafe"

    return ModerationResult(
        text=text,
        categories=categories,
        overall_decision=overall_decision,
        raw_response=response.as_dict()
    )
