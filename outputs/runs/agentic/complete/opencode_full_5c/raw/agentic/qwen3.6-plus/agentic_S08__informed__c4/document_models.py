from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ExtractedField:
    name: str
    value: Optional[str] = None
    confidence: float = 0.0


@dataclass
class InvoiceExtractionResult:
    vendor: ExtractedField = field(default_factory=lambda: ExtractedField("vendor"))
    invoice_date: ExtractedField = field(
        default_factory=lambda: ExtractedField("invoice_date")
    )
    total: ExtractedField = field(default_factory=lambda: ExtractedField("total"))
    line_items: list = field(default_factory=list)
    raw_response: Optional[dict] = None

    def to_dict(self):
        return {
            "vendor": asdict(self.vendor),
            "invoice_date": asdict(self.invoice_date),
            "total": asdict(self.total),
            "line_items": self.line_items,
        }


@dataclass
class ReceiptExtractionResult:
    merchant: ExtractedField = field(default_factory=lambda: ExtractedField("merchant"))
    tax: ExtractedField = field(default_factory=lambda: ExtractedField("tax"))
    total: ExtractedField = field(default_factory=lambda: ExtractedField("total"))
    items: list = field(default_factory=list)
    raw_response: Optional[dict] = None

    def to_dict(self):
        return {
            "merchant": asdict(self.merchant),
            "tax": asdict(self.tax),
            "total": asdict(self.total),
            "items": self.items,
        }


@dataclass
class NormalizedExpense:
    document_type: str = ""
    vendor_or_merchant: str = ""
    date: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    line_items: list = field(default_factory=list)
    currency: str = "USD"
    confidence: float = 0.0
    source_document: str = ""

    def to_dict(self):
        return asdict(self)


def normalize_invoice_result(
    invoice_result: InvoiceExtractionResult,
) -> NormalizedExpense:
    normalized = NormalizedExpense(
        document_type="invoice",
        vendor_or_merchant=invoice_result.vendor.value or "",
        date=invoice_result.invoice_date.value or "",
        total=_parse_float(invoice_result.total.value),
        line_items=invoice_result.line_items,
        confidence=min(
            invoice_result.vendor.confidence,
            invoice_result.invoice_date.confidence,
            invoice_result.total.confidence,
        ),
    )
    return normalized


def normalize_receipt_result(
    receipt_result: ReceiptExtractionResult,
) -> NormalizedExpense:
    normalized = NormalizedExpense(
        document_type="receipt",
        vendor_or_merchant=receipt_result.merchant.value or "",
        date="",
        tax=_parse_float(receipt_result.tax.value),
        total=_parse_float(receipt_result.total.value),
        line_items=receipt_result.items,
        confidence=min(
            receipt_result.merchant.confidence,
            receipt_result.tax.confidence,
            receipt_result.total.confidence,
        ),
    )
    return normalized


def _parse_float(value) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).replace(",", "").replace("$", "").strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return 0.0


REQUIRED_INVOICE_FIELDS = ["vendor", "invoice_date", "total"]
REQUIRED_RECEIPT_FIELDS = ["merchant", "tax", "total"]
MINIMUM_CONFIDENCE = 0.5


def validate_invoice_fields(result_dict: dict) -> dict:
    errors = []
    field_confidences = {}
    for field_name in REQUIRED_INVOICE_FIELDS:
        field_data = result_dict.get(field_name, {})
        value = field_data.get("value")
        confidence = field_data.get("confidence", 0.0)
        field_confidences[field_name] = confidence
        if not value:
            errors.append(f"Missing required invoice field: {field_name}")
        elif confidence < MINIMUM_CONFIDENCE:
            errors.append(
                f"Low confidence for field '{field_name}': {confidence:.2f} < {MINIMUM_CONFIDENCE}"
            )
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "confidences": field_confidences,
    }


def validate_receipt_fields(result_dict: dict) -> dict:
    errors = []
    field_confidences = {}
    for field_name in REQUIRED_RECEIPT_FIELDS:
        field_data = result_dict.get(field_name, {})
        value = field_data.get("value")
        confidence = field_data.get("confidence", 0.0)
        field_confidences[field_name] = confidence
        if not value:
            errors.append(f"Missing required receipt field: {field_name}")
        elif confidence < MINIMUM_CONFIDENCE:
            errors.append(
                f"Low confidence for field '{field_name}': {confidence:.2f} < {MINIMUM_CONFIDENCE}"
            )
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "confidences": field_confidences,
    }
