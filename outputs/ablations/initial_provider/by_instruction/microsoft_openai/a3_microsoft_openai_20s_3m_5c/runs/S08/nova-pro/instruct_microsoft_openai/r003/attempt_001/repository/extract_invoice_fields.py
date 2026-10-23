import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from.document_models import DocumentRequest, DocumentResponse, NormalizedExpense

def extract_invoice_fields(document_path: str):
    client = get_document_intelligence_client()
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document("prebuilt-invoice", document_file)
        result = poller.result()
        response = DocumentResponse(result)
        vendor = response.result['vendorName']['value']
        date = response.result['fields']['InvoiceDate']['value']
        total = response.result['fields']['Total']['value']
        items = {item['productCode']['value']: item['quantity']['value'] for item in response.result['items']}
        return NormalizedExpense(vendor, date, total, items)