import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature

def extract_text(image_path):
    client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'), credential=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY'))
    with open(image_path, "rb") as image_file:
        poller = client.begin_analyze_document('prebuilt-document', AnalyzeDocumentRequest(document=image_file))
        result = poller.result()
        text = ' '.join([line.content for line in result.paragraphs])
        return text