import os
from typing import Dict, Any, List, Optional
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential


def extract_invoice_fields(invoice_path: str) -> Dict[str, Any]:
    """
    Extract vendor, date, total, and line-item fields from an invoice using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(invoice_path, "rb") as f:
        document_content = f.read()

    poller = client.begin_analyze_document(
        "prebuilt-invoice", AnalyzeDocumentRequest(bytes_source=document_content)
    )
    result = poller.result()

    extracted_fields = {"vendor": None, "date": None, "total": None, "line_items": []}

    if result.documents:
        invoice = result.documents[0]
        fields = invoice.fields

        if "VendorName" in fields:
            extracted_fields["vendor"] = fields["VendorName"].value_string

        if "InvoiceDate" in fields:
            extracted_fields["date"] = fields["InvoiceDate"].value_date

        if "InvoiceTotal" in fields:
            extracted_fields["total"] = float(fields["InvoiceTotal"].value_number)

        if "Items" in fields:
            items = fields["Items"].value_array
            for item in items:
                item_fields = item.value_object
                line_item = {}
                if "Description" in item_fields:
                    line_item["description"] = item_fields["Description"].value_string
                if "Amount" in item_fields:
                    line_item["amount"] = float(item_fields["Amount"].value_number)
                if "Quantity" in item_fields:
                    line_item["quantity"] = float(item_fields["Quantity"].value_number)
                extracted_fields["line_items"].append(line_item)

    return extracted_fields
