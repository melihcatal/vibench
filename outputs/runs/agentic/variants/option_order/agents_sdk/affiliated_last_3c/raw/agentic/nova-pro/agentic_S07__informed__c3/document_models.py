from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

def create_analyze_request(document):
    return AnalyzeDocumentRequest(document=document)