import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

class DocumentClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
            key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
            if not endpoint or not key:
                raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set.")
            cls._instance = DocumentIntelligenceClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(key)
            )
        return cls._instance

def analyze_document(model_id: str, image_path: str) -> dict:
    client = DocumentClient()
    with open(image_path, 'rb') as f:
        data = f.read()
    poller = client.begin_analyze_document(model_id, AnalyzeDocumentRequest(data))
    result = poller.result()
    return result.to_dict()