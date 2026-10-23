import os
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_client():
    conn_str = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_CONNECTION_STRING')
    return DocumentIntelligenceClient.from_connection_string(conn_str)
