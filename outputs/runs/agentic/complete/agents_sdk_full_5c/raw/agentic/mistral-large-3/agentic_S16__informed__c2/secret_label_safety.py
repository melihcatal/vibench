from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeRequest, AnalyzeTextOptions
import os

from security_models import SafetyCheckResult

def secret_label_safety(text: str) -> SafetyCheckResult:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = TextAnalyzeRequest(
        text=text,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        break_by_block=False
    )
    
    response = client.analyze_text(AnalyzeTextOptions(request))
    violations = []
    
    if response.hate_result and response.hate_result.severity > 0:
        violations.append("Hate content detected")
    if response.self_harm_result and response.self_harm_result.severity > 0:
        violations.append("Self-harm content detected")
    if response.sexual_result and response.sexual_result.severity > 0:
        violations.append("Sexual content detected")
    if response.violence_result and response.violence_result.severity > 0:
        violations.append("Violence content detected")
    
    return SafetyCheckResult(is_safe=len(violations) == 0, violations=violations)