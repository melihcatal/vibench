import os
import json
from typing import Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from document_models import ExtractedReceipt, LineItem


def extract_receipt_fields(document_path: str) -> ExtractedReceipt:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-receipt",
            document=f.read(),
            content_type="application/octet-stream",
        )
    result: AnalyzeResult = poller.result()
    fields_dict = result.fields.get_field_dict() if result.fields else {}
    merchant_name = (
        fields_dict.get("MerchantName", {}).content
        if "MerchantName" in fields_dict
        else None
    )
    transaction_date = (
        fields_dict.get("TransactionDate", {}).content
        if "TransactionDate" in fields_dict
        else None
    )
    total_str = fields_dict.get("Total", {}).content if "Total" in fields_dict else None
    total = float(total_str) if total_str else None
    tax_str = (
        fields_dict.get("TotalTax", {}).content if "TotalTax" in fields_dict else None
    )
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
    return ExtractedReceipt(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total=total,
        tax=tax,
        line_items=line_items,
        confidence=confidence,
    )
