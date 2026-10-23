from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def moderate_vendor_text(text):
    client = ContentSafetyClient(
        endpoint="https://<your-custom-subdomain>.cognitiveservices.azure.com/", credential=AzureKeyCredential("<your-api-key>")
    )
    result = client.classify_text(text)
    return result