from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_document_intelligence_client(config):
    return DocumentIntelligenceClient(
        endpoint=config['document_intelligence_endpoint'],
        credential=AzureKeyCredential(config['document_intelligence_api_key'])
    )
