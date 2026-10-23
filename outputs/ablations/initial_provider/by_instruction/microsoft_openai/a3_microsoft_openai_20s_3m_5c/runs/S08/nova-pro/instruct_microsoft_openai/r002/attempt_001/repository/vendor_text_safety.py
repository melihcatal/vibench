from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def moderate_vendor_text(vendor_text):
    client = ContentSafetyClient(
        endpoint="https://<your-custom-subdomain>.cognitiveservices.azure.com",
        credential=AzureKeyCredential("<your-api-key>")
    )
    result = client.text_moderation(vendor_text)
    return result.severity