import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from.document_models import DocumentRequest, DocumentResponse

def extract_receipt_fields(document_path: str):
    client = get_document_intelligence_client()
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document("prebuilt-receipt", document_file)
        result = poller.result()
        response = DocumentResponse(result)
        merchant = response.result['merchantName']['value']
        tax = response.result['fields']['Tax']['value']
        total = response.result['fields']['Total']['value']
        items = {item['name']['value']: item['quantity']['value'] for item in response.result['items']}
        return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}