from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def check_safety(text):
    client = ContentSafetyClient(endpoint='https://<your-resource-name>.cognitiveservices.azure.com/', credential=AzureKeyCredential('<your-api-key>'))
    result = client.classify_text(text)
    return result
