from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

def check_safety(text):
    client = DocumentIntelligenceClient.from_connection_string(conn_str="YOUR_CONNECTION_STRING")
    # Placeholder for actual safety check logic
    return f"Safety check result: {text}"
