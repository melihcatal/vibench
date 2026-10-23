from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

def check_safety(text):
    client = ContentSafetyClient(endpoint="https://<your-resource-name>.cognitiveservices.azure.com/", credential=AzureKeyCredential("<your-api-key>"))
    result = client.analyze_text(AnalyzeTextOptions(text))
    return result.results[0].severity if result.results else ""