import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from messaging_models import EventMessage

endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

def check_message_safety(event: EventMessage) -> bool:
    text = str(event.payload)
    
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)
    
    return all(
        result.severity <= 2
        for result in [
            response.hate_result,
            response.self_harm_result,
            response.sexual_result,
            response.violence_result
        ]
    )