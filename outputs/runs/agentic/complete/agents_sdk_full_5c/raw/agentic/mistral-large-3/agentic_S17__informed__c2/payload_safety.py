from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalysisRequest, AnalyzeTextOptions
from security_models import SafetyCheckRequest, SafetyCheckResponse
import os

def check_payload_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    analysis_request = AnalyzeTextOptions(
        text=request.text,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"]
    )
    
    response = client.analyze_text(analysis_request)
    
    return SafetyCheckResponse(
        is_safe=all(
            result.severity < 2 for result in response.categories_analysis
        ),
        details=response.categories_analysis
    )