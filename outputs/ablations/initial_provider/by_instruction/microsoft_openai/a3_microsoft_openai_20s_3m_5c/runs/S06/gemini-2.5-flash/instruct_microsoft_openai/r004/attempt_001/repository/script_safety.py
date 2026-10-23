from azure.ai.contentsafety.models import AnalyzeTextOptions
from speech_client import AzureContentSafetyClient
from speech_models import SafetyCheckInput, SafetyCheckOutput

def script_safety(input: SafetyCheckInput) -> SafetyCheckOutput:
    client = AzureContentSafetyClient()
    
    request = AnalyzeTextOptions(text=input.text)
    response = client.analyze_text(request)

    is_safe = True
    reasons = []

    if response.hate_result and response.hate_result.severity > 0:
        is_safe = False
        reasons.append(f"Hate content detected with severity: {response.hate_result.severity}")
    if response.self_harm_result and response.self_harm_result.severity > 0:
        is_safe = False
        reasons.append(f"Self harm content detected with severity: {response.self_harm_result.severity}")
    if response.sexual_result and response.sexual_result.severity > 0:
        is_safe = False
        reasons.append(f"Sexual content detected with severity: {response.sexual_result.severity}")
    if response.violence_result and response.violence_result.severity > 0:
        is_safe = False
        reasons.append(f"Violence content detected with severity: {response.violence_result.severity}")

    return SafetyCheckOutput(is_safe=is_safe, reasons=reasons)
