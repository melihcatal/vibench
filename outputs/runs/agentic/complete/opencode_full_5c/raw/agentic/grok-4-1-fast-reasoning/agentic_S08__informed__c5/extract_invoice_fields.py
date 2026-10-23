import os
import json
from typing import Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from document_models import ExtractedInvoice, LineItem


def extract_invoice_fields(document_path: str) -> ExtractedInvoice:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=f.read(),
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()
    fields_dict = result.fields.get_field_dict() if result.fields else {}
    vendor_name = (
        fields_dict.get("VendorName", {}).content
        if "VendorName" in fields_dict
        else None
    )
    invoice_date = (
        fields_dict.get("DocumentDate", {}).content
        if "DocumentDate" in fields_dict
        else None
    )
    due_date = (
        fields_dict.get("DueDate", {}).content if "DueDate" in fields_dict else None
    )
    total_str = (
        fields_dict.get("AmountDue", {}).content if "AmountDue" in fields_dict else None
    )
    total = float(total_str) if total_str else None
    tax_str = fields_dict.get("Tax", {}).content if "Tax" in fields_dict else None
    tax = float(tax_str) if tax_str else None
    line_items: list[LineItem] = []
    if result.tables:
        for table in result.tables:
            if table.row_count > 1:
                for row in range(1, table.row_count):
                    cells = {
                        cell.column_index: cell.content
                        for cell in table.cells
                        if cell.row_index == row
                    }
                    item = LineItem(
                        description=cells.get(0),
                        quantity=float(cells.get(1))
                        if 1 in cells and cells[1]
                        else None,
                        unit_price=float(cells.get(2))
                        if 2 in cells and cells[2]
                        else None,
                        amount=float(cells.get(3)) if 3 in cells and cells[3] else None,
                    )
                    line_items.append(item)
    confidence = {
        k: v.confidence
        for k, v in fields_dict.items()
        if hasattr(v, "confidence") and v.confidence is not None
    }
    return ExtractedInvoice(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        due_date=due_date,
        total=total,
        tax=tax,
        line_items=line_items,
        confidence=confidence,
    )
