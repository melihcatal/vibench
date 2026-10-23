import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

client = DocumentIntelligenceClient(endpoint=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'), credential=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY'))

def extract_invoice_fields(invoice_path):
    with open(invoice_path, "rb") as f:
        poller = client.begin_analyze_document('prebuilt-invoice', document=f)
    result = poller.result()
    return result