import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature

client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'), credential=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY'))

def extract_tables(document_path):
    with open(document_path, 'rb') as document_file:
        poller = client.begin_analyze_document('prebuilt-document', AnalyzeDocumentRequest(document=document_file))
        result = poller.result()
        return result.tables