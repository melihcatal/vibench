import os
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_document_client():
    return DocumentIntelligenceClient(
        endpoint=os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT'),
        credential=os.getenv('DOCUMENT_INTELLIGENCE_KEY')
    )