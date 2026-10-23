from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    amount: float
    confidence: float = 1.0


@dataclass
class ExtractedInvoiceFields:
    vendor_name: str
    vendor_address: str
    invoice_id: str
    invoice_date: str
    due_date: str
    total: float
    subtotal: float
    tax: float
    line_items: List[LineItem]
    confidence_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class ExtractedReceiptFields:
    merchant_name: str
    merchant_address: str
    transaction_date: str
    transaction_time: str
    total: float
    subtotal: float
    tax: float
    items: List[LineItem]
    confidence_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    document_type: str
    vendor_or_merchant: str
    document_id: str
    date: str
    total_amount: float
    tax_amount: float
    subtotal: float
    line_items: List[Dict[str, Any]]
    currency: str
    confidence: float
    normalized_at: str


@dataclass
class ValidationReport:
    is_valid: bool
    missing_fields: List[str]
    low_confidence_fields: List[str]
    confidence_threshold: float = 0.7
    details: Dict[str, Any] = field(default_factory=dict)


def parse_invoice_from_azure_result(result) -> ExtractedInvoiceFields:
    doc = result.documents[0] if result.documents else None
    if not doc:
        raise ValueError("No document found in Azure Form Recognizer result")

    fields = doc.fields
    vendor_name = fields.get("VendorName", {}).get("value", "")
    vendor_address = fields.get("VendorAddress", {}).get("value", "")
    invoice_id = fields.get("InvoiceId", {}).get("value", "")
    invoice_date = fields.get("InvoiceDate", {}).get("value", "")
    due_date = fields.get("DueDate", {}).get("value", "")
    total = fields.get("InvoiceTotal", {}).get("value", 0.0)
    subtotal = fields.get("SubTotal", {}).get("value", 0.0)
    tax = fields.get("TotalTax", {}).get("value", 0.0)

    line_items = []
    items_field = fields.get("Items", {}).get("valueArray", [])
    for item in items_field:
        item_fields = item.get("valueObject", {})
        line_items.append(
            LineItem(
                description=item_fields.get("Description", {}).get("value", ""),
                quantity=item_fields.get("Quantity", {}).get("value", 0.0),
                unit_price=item_fields.get("UnitPrice", {}).get("value", 0.0),
                amount=item_fields.get("Amount", {}).get("value", 0.0),
                confidence=item_fields.get("Amount", {}).get("confidence", 1.0),
            )
        )

    confidence_scores = {
        "vendor_name": fields.get("VendorName", {}).get("confidence", 0.0),
        "invoice_date": fields.get("InvoiceDate", {}).get("confidence", 0.0),
        "total": fields.get("InvoiceTotal", {}).get("confidence", 0.0),
        "tax": fields.get("TotalTax", {}).get("confidence", 0.0),
    }

    return ExtractedInvoiceFields(
        vendor_name=vendor_name,
        vendor_address=vendor_address,
        invoice_id=invoice_id,
        invoice_date=invoice_date,
        due_date=due_date,
        total=total,
        subtotal=subtotal,
        tax=tax,
        line_items=line_items,
        confidence_scores=confidence_scores,
    )


def parse_receipt_from_azure_result(result) -> ExtractedReceiptFields:
    doc = result.documents[0] if result.documents else None
    if not doc:
        raise ValueError("No document found in Azure Form Recognizer result")

    fields = doc.fields
    merchant_name = fields.get("MerchantName", {}).get("value", "")
    merchant_address = fields.get("MerchantAddress", {}).get("value", "")
    transaction_date = fields.get("TransactionDate", {}).get("value", "")
    transaction_time = fields.get("TransactionTime", {}).get("value", "")
    total = fields.get("Total", {}).get("value", 0.0)
    subtotal = fields.get("Subtotal", {}).get("value", 0.0)
    tax = fields.get("TotalTax", {}).get("value", 0.0)

    items = []
    items_field = fields.get("Items", {}).get("valueArray", [])
    for item in items_field:
        item_fields = item.get("valueObject", {})
        items.append(
            LineItem(
                description=item_fields.get("Description", {}).get("value", ""),
                quantity=item_fields.get("Quantity", {}).get("value", 0.0),
                unit_price=item_fields.get("Price", {}).get("value", 0.0),
                amount=item_fields.get("TotalPrice", {}).get("value", 0.0),
                confidence=item_fields.get("TotalPrice", {}).get("confidence", 1.0),
            )
        )

    confidence_scores = {
        "merchant_name": fields.get("MerchantName", {}).get("confidence", 0.0),
        "transaction_date": fields.get("TransactionDate", {}).get("confidence", 0.0),
        "total": fields.get("Total", {}).get("confidence", 0.0),
        "tax": fields.get("TotalTax", {}).get("confidence", 0.0),
    }

    return ExtractedReceiptFields(
        merchant_name=merchant_name,
        merchant_address=merchant_address,
        transaction_date=transaction_date,
        transaction_time=transaction_time,
        total=total,
        subtotal=subtotal,
        tax=tax,
        items=items,
        confidence_scores=confidence_scores,
    )


def normalize_expense_record(
    extracted_data, document_type: str, currency: str = "USD"
) -> NormalizedExpenseRecord:
    if document_type == "invoice":
        vendor_or_merchant = extracted_data.vendor_name
        document_id = extracted_data.invoice_id
        date = extracted_data.invoice_date
        total_amount = extracted_data.total
        tax_amount = extracted_data.tax
        subtotal = extracted_data.subtotal
        line_items = [asdict(item) for item in extracted_data.line_items]
        confidence = extracted_data.confidence_scores.get("total", 0.0)
    elif document_type == "receipt":
        vendor_or_merchant = extracted_data.merchant_name
        document_id = f"RCP-{extracted_data.transaction_date}"
        date = extracted_data.transaction_date
        total_amount = extracted_data.total
        tax_amount = extracted_data.tax
        subtotal = extracted_data.subtotal
        line_items = [asdict(item) for item in extracted_data.items]
        confidence = extracted_data.confidence_scores.get("total", 0.0)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")

    return NormalizedExpenseRecord(
        document_type=document_type,
        vendor_or_merchant=vendor_or_merchant,
        document_id=document_id,
        date=date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        subtotal=subtotal,
        line_items=line_items,
        currency=currency,
        confidence=confidence,
        normalized_at=datetime.utcnow().isoformat(),
    )
