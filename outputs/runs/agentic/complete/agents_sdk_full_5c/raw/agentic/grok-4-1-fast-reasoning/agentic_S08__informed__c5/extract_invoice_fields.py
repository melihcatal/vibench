import os
from typing import Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from document_models import DocumentFields, LineItem
from document_client import document_bytes_from_path

def extract_invoice_fields(document_input: str | bytes) -> DocumentFields:
    if isinstance(document_input, str):
        document_bytes = document_bytes_from_path(document_input)
    else:
        document_bytes = document_input
    
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        document=AnalyzeDocumentRequest(bytes_source=document_bytes)
    )
    result = poller.result()
    
    fields_dict: Dict[str, Any] = {"line_items": [], "confidence": {}}
    
    vendor_field = result.fields.get("VendorName")
    if vendor_field:
        fields_dict["vendor"] = vendor_field.content
        fields_dict["confidence"]["vendor"] = vendor_field.confidence
    
    date_field = result.fields.get("InvoiceDate")
    if date_field:
        fields_dict["date"] = date_field.content
        fields_dict["confidence"]["date"] = date_field.confidence
    
    total_field = result.fields.get("AmountDue") or result.fields.get("InvoiceTotal")
    if total_field and total_field.content:
        fields_dict["total"] = float(total_field.content)
        fields_dict["confidence"]["total"] = total_field.confidence
    
    # Simplified line items from tables
    if result.tables:
        table = result.tables[0]  # Assume first table is line items
        for i in range(table.row_count):
            # Basic parsing
            desc = f"Item {i+1}"
            amount = 0.0
            fields_dict["line_items"].append(LineItem(description=desc, amount=amount))
    
    return DocumentFields(**fields_dict)