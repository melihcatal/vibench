from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

def create_analyze_request(image_path, document_type):
    with open(image_path, "rb") as image_file:
        return AnalyzeDocumentRequest(
            document_type=document_type,
            content=image_file.read()
        )
