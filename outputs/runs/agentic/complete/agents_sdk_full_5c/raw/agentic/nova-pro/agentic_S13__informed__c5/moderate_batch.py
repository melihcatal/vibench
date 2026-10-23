from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(endpoint='AZURE_CONTENT_SAFETY_ENDPOINT', credential=AzureKeyCredential('AZURE_CONTENT_SAFETY_KEY'))

def moderate_batch(texts):
    results = []
    for text in texts:
        response = client.analyze_text(AnalyzeTextOptions(text=text))
        results.append(response.as_dict())
    return results
