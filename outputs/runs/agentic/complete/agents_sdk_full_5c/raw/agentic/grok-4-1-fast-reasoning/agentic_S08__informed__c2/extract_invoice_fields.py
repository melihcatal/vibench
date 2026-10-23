import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import load_document_bytes, detect_mime_type
from document_models import InvoiceFields, ExtractedField, LineItem
from typing import List

def extract_invoice_fields(document_path: str) -> InvoiceFields:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError("Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY")

    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    bytes_data = load_document_bytes(document_path)
    mime_type = detect_mime_type(document_path)
    
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        document=bytes_data,
        content_type=mime_type
    )
    result: AnalyzeResult = poller.result()
    
    fields: InvoiceFields = {
        "vendor_name": ExtractedField(value="", confidence=0.0),
        "invoice_date": ExtractedField(value="", confidence=0.0),
        "total_amount": ExtractedField(value=0.0, confidence=0.0),
        "line_items": []
    }
    
    vendor_field = next((f for f in result.fields if f.name.lower() == "vendorname"), None)
    if vendor_field and vendor_field.content:
        fields["vendor_name"] = ExtractedField(value=str(vendor_field.content), confidence=vendor_field.confidence or 0.0)
    
    date_field = next((f for f in result.fields if "date" in f.name.lower()), None)
    if date_field and date_field.content:
        fields["invoice_date"] = ExtractedField(value=str(date_field.content), confidence=date_field.confidence or 0.0)
    
    total_candidates = ["amountdue", "invoicetotal", "total"]
    total_field = next((f for f in result.fields if any(cand in f.name.lower() for cand in total_candidates)), None)
    if total_field and total_field.content:
        fields["total_amount"] = ExtractedField(value=float(str(total_field.content)), confidence=total_field.confidence or 0.0)
    
    line_items: List[LineItem] = []
    if result.tables:
        for table in result.tables:
            for cell in table.cells:
                if "item" in cell.content.lower() or "description" in cell.content.lower():
                    # Simplified line item extraction
                    line_items.append(LineItem(description=str(cell.content), quantity=None, price=0.0, confidence=cell.confidence or 0.0))
    fields["line_items"] = line_items
    
    return fields