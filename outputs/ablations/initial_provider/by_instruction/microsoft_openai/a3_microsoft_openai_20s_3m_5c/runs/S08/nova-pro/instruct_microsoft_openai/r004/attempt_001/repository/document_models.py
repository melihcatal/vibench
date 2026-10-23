from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

def create_analyze_request(document_path, document_type):
    with open(document_path, 'rb') as document_file:
        return AnalyzeDocumentRequest(document=document_file, model_id=document_type)