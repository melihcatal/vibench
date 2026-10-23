from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_client():
    return DocumentIntelligenceClient(
        endpoint="https://<your-custom-subdomain>.cognitiveservices.azure.com/", credential=AzureKeyCredential("<your-api-key>")
    )