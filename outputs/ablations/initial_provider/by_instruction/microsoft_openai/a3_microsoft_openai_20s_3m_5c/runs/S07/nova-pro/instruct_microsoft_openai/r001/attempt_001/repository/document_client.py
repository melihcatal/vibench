import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature

class DocumentClient:
    def __init__(self):
        self.client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'), credential=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY'))

    def analyze_document(self, image_path):
        with open(image_path, "rb") as image_file:
            poller = self.client.begin_analyze_document('prebuilt-document', AnalyzeDocumentRequest(document=image_file))
            return poller.result()