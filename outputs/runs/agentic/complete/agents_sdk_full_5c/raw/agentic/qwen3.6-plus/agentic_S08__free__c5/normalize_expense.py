"""
Normalize extracted expense fields into a standard JSON schema using Google Cloud Document AI.
Provider: Google Cloud Document AI (Expense Processing Processor)
"""

import os
import json
from typing import Optional, Dict, Any, List
from google.cloud import documentai
from google.cloud.documentai_toolbox import wrappers
from google.api_core.client_options import ClientOptions

from document_models import (
    ExpenseRecord,
    NormalizedExpenseRequest,
    NormalizedExpenseResponse,
    LineItem,
    ReceiptItem,
)


def normalize_expense(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
    document_path: Optional[str] = None,
    document_bytes: Optional[bytes] = None,
    mime_type: str = "application/pdf",
    extracted_data: Optional[Dict[str, Any]] = None,
) -> NormalizedExpenseResponse:
    """
    Normalize extracted expense data into a standardized schema using Google Cloud Document AI.
    
    When raw document is provided, uses Google Document AI expense processor (e.g., 
    `expense-processor` or custom processor) to extract and normalize.
    When extracted_data is provided, normalizes the pre-extracted data into standard schema.
    
    Args:
        project_id: Google Cloud project ID
        location: Google Cloud location (e.g., us, eu)
        processor_id: Document AI processor ID (e.g., expense-processor or a custom ID)
        document_path: Path to document file
        document_bytes: Raw document bytes
        mime_type: MIME type of the document
        extracted_data: Pre-extracted fields to normalize
    
    Returns:
        NormalizedExpenseResponse with standardized expense record
    """
    if extracted_data:
        expense_record = _normalize_from_extracted(extracted_data)
        return NormalizedExpenseResponse(
            expense=expense_record,
            normalized=True,
        )

    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    loc = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    proc_id = processor_id or os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "expense-processor")
    
    if not project:
        raise ValueError("Google Cloud project ID must be provided or set via GOOGLE_CLOUD_PROJECT")
    
    opts = ClientOptions(api_endpoint=f"{loc}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    name = client.processor_path(project, loc, proc_id)
    
    if document_bytes:
        raw_document_bytes = document_bytes
    elif document_path:
        with open(document_path, "rb") as f:
            raw_document_bytes = f.read()
    else:
        raise ValueError("Either document_path, document_bytes, or extracted_data must be provided")
    
    document = documentai.RawDocument(content=raw_document_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=document)
    
    result = client.process_document(request=request)
    expense_record = _normalize_from_docai_result(result.document)
    
    return NormalizedExpenseResponse(
        expense=expense_record,
        normalized=True,
    )


def _normalize_from_docai_result(document: Any) -> ExpenseRecord:
    """Normalize Google Document AI process result into ExpenseRecord."""
    fields = {}
    if hasattr(document, "entities"):
        for entity in document.entities:
            if hasattr(entity, "mention_text") and entity.mention_text:
                entity_type = entity.type_ if hasattr(entity, "type_") else "unknown"
                normalized_type = _map_docai_entity_type(entity_type)
                fields[normalized_type] = entity.mention_text
    
    vendor = fields.get("vendor") or fields.get("supplier")
    invoice_date = fields.get("invoice_date") or fields.get("date")
    total = _parse_amount(fields.get("total"))
    tax = _parse_amount(fields.get("tax"))
    currency = fields.get("currency", "USD")
    
    line_items: List[LineItem] = []
    if hasattr(document, "entities"):
        for entity in document.entities:
            if entity.type_ == "line_item":
                li = LineItem(
                    description=_get_entity_prop(entity, "description"),
                    quantity=_get_entity_prop(entity, "quantity"),
                    unit_price=_parse_amount(_get_entity_prop(entity, "amount")),
                    line_total=_parse_amount(_get_entity_prop(entity, "total")),
                )
                line_items.append(li)
    
    return ExpenseRecord(
        vendor=vendor,
        date=invoice_date,
        total_amount=total,
        tax_amount=tax,
        currency=currency,
        line_items=line_items,
        document_type=_detect_document_type(fields),
    )


def _normalize_from_extracted(data: Dict[str, Any]) -> ExpenseRecord:
    """Normalize pre-extracted dictionary into standard ExpenseRecord."""
    vendor = data.get("vendor") or data.get("merchant")
    invoice_date = data.get("invoice_date") or data.get("transaction_date") or data.get("date")
    
    total = data.get("total_amount") or data.get("total")
    if isinstance(total, str):
        total = _parse_amount(total)
    
    tax = data.get("tax_amount") or data.get("tax")
    if isinstance(tax, str):
        tax = _parse_amount(tax)
    
    currency = data.get("currency", "USD")
    
    raw_items = data.get("line_items") or data.get("items") or []
    line_items: List[LineItem] = []
    for item in raw_items:
        if isinstance(item, LineItem):
            line_items.append(item)
        elif isinstance(item, ReceiptItem):
            line_items.append(
                LineItem(
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=item.total_price,
                )
            )
        elif isinstance(item, dict):
            line_items.append(
                LineItem(
                    description=item.get("description") or item.get("item"),
                    quantity=item.get("quantity"),
                    unit_price=item.get("unit_price"),
                    line_total=item.get("line_total") or item.get("total_price"),
                )
            )
    
    doc_type = _detect_document_type(data)
    
    return ExpenseRecord(
        vendor=vendor,
        date=invoice_date,
        total_amount=total,
        tax_amount=tax,
        currency=currency,
        line_items=line_items,
        document_type=doc_type,
        metadata=data.get("metadata", {}),
    )


def _parse_amount(value: Any) -> Optional[float]:
    """Parse amount string or value into float."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).replace("$", "").replace(",", "").replace("€", "").strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def _map_docai_entity_type(entity_type: str) -> str:
    """Map Document AI entity type to standard field name."""
    mapping = {
        "supplier_name": "vendor",
        "vendor_name": "vendor",
        "invoice_date": "invoice_date",
        "transaction_date": "invoice_date",
        "invoice_total": "total",
        "total_amount": "total",
        "total_tax": "tax",
        "tax_amount": "tax",
        "currency_code": "currency",
        "line_item": "line_item",
    }
    return mapping.get(entity_type, entity_type)


def _get_entity_prop(entity: Any, prop_name: str) -> Optional[str]:
    """Get a property value from a Document AI entity."""
    if hasattr(entity, "properties"):
        for prop in entity.properties:
            if prop.type_ == prop_name:
                return prop.mention_text if hasattr(prop, "mention_text") else None
    return None


def _detect_document_type(fields: Dict[str, Any]) -> str:
    """Detect document type from extracted fields."""
    if fields.get("receipt_number") or fields.get("transaction_date"):
        return "receipt"
    if fields.get("invoice_number") or fields.get("invoice_date"):
        return "invoice"
    return "expense_document"


if __name__ == "__main__":
    sample_data = {
        "vendor": "Office Supplies Co.",
        "date": "2024-01-15",
        "total_amount": 125.50,
        "tax_amount": 10.50,
        "currency": "USD",
        "line_items": [
            {"description": "Printer Paper", "quantity": 5, "unit_price": 12.00, "line_total": 60.00},
            {"description": "Pens (box)", "quantity": 2, "unit_price": 15.50, "line_total": 31.00},
        ],
    }
    
    result = normalize_expense(extracted_data=sample_data)
    print(result.model_dump_json(indent=2))
