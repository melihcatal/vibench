from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import os

def check_message_safety(text: str) -> Dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text, categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE])
    response = client.analyze_text(request)
    
    return {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity
    }