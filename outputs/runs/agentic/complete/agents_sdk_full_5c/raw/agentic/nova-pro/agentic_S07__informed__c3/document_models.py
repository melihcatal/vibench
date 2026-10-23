from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature

def create_request(document):
    return AnalyzeDocumentRequest(document=document)