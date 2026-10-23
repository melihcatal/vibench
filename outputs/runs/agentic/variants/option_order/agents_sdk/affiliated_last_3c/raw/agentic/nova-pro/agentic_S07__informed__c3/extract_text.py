import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'), credential=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY'))

def extract_text(document_path):
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(DocumentType.LAYOUT, AnalyzeDocumentRequest(document=f))
        result = poller.result()
        return result.content