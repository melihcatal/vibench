from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

def extract_tables(image_path):
    client = DocumentIntelligenceClient.from_connection_string(conn_str="YOUR_CONNECTION_STRING")
    with open(image_path, "rb") as image_file:
        poller = client.begin_analyze_document(
            AnalyzeDocumentRequest(
                document_type=DocumentType.LAYOUT,
                content=image_file.read()
            )
        )
        result = poller.result()
        return result.tables
