from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class FieldConfidence(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ExtractedField:
    """Represents an extracted field with confidence."""

    name: str
    value: Any
    confidence: float
    raw_text: Optional[str] = None
    bounding_box: Optional[Dict[str, float]] = None


@dataclass
class LineItem:
    """Represents a line item in an invoice or receipt."""

    description: str
    quantity: float
    unit_price: float
    total_price: float
    confidence: float


@dataclass
class InvoiceData:
    """Normalized invoice data."""

    vendor_name: str
    invoice_date: str
    invoice_number: str
    total_amount: float
    tax_amount: float
    subtotal: float
    line_items: List[LineItem]
    extracted_fields: List[ExtractedField] = field(default_factory=list)
    confidence_score: float = 0.0


@dataclass
class ReceiptData:
    """Normalized receipt data."""

    merchant_name: str
    transaction_date: str
    total_amount: float
    tax_amount: float
    items: List[Dict[str, Any]]
    extracted_fields: List[ExtractedField] = field(default_factory=list)
    confidence_score: float = 0.0


@dataclass
class ExpenseRecord:
    """Normalized expense record for storage."""

    document_type: str
    vendor: str
    date: str
    total: float
    currency: str
    line_items: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    confidence: float = 0.0


class DocumentNormalizer:
    """Helper for normalizing extracted document data."""

    @staticmethod
    def normalize_invoice_from_textract(
        textract_response: Dict[str, Any],
    ) -> InvoiceData:
        """Normalize Textract AnalyzeExpense response to InvoiceData."""
        invoice_data = InvoiceData(
            vendor_name="",
            invoice_date="",
            invoice_number="",
            total_amount=0.0,
            tax_amount=0.0,
            subtotal=0.0,
            line_items=[],
            confidence_score=0.0,
        )

        extracted_fields = []
        line_items = []

        if "ExpenseDocuments" in textract_response:
            for expense_doc in textract_response["ExpenseDocuments"]:
                for summary_field in expense_doc.get("SummaryFields", []):
                    field_type = summary_field.get("Type", {}).get("Text", "").lower()
                    field_text = summary_field.get("ValueDetection", {}).get("Text", "")
                    confidence = summary_field.get("ValueDetection", {}).get(
                        "Confidence", 0.0
                    )

                    extracted_fields.append(
                        ExtractedField(
                            name=field_type,
                            value=field_text,
                            confidence=confidence,
                            raw_text=field_text,
                        )
                    )

                    if "vendor" in field_type:
                        invoice_data.vendor_name = field_text
                    elif "date" in field_type:
                        invoice_data.invoice_date = field_text
                    elif "invoice" in field_type and "number" in field_type:
                        invoice_data.invoice_number = field_text
                    elif "total" in field_type:
                        try:
                            invoice_data.total_amount = float(
                                field_text.replace("$", "").replace(",", "")
                            )
                        except:
                            pass
                    elif "tax" in field_type:
                        try:
                            invoice_data.tax_amount = float(
                                field_text.replace("$", "").replace(",", "")
                            )
                        except:
                            pass
                    elif "subtotal" in field_type:
                        try:
                            invoice_data.subtotal = float(
                                field_text.replace("$", "").replace(",", "")
                            )
                        except:
                            pass

        invoice_data.extracted_fields = extracted_fields
        invoice_data.line_items = line_items

        if extracted_fields:
            invoice_data.confidence_score = sum(
                f.confidence for f in extracted_fields
            ) / len(extracted_fields)

        return invoice_data

    @staticmethod
    def normalize_receipt_from_textract(
        textract_response: Dict[str, Any],
    ) -> ReceiptData:
        """Normalize Textract AnalyzeExpense response to ReceiptData."""
        receipt_data = ReceiptData(
            merchant_name="",
            transaction_date="",
            total_amount=0.0,
            tax_amount=0.0,
            items=[],
        )

        extracted_fields = []
        items = []

        if "ExpenseDocuments" in textract_response:
            for expense_doc in textract_response["ExpenseDocuments"]:
                for summary_field in expense_doc.get("SummaryFields", []):
                    field_type = summary_field.get("Type", {}).get("Text", "").lower()
                    field_text = summary_field.get("ValueDetection", {}).get("Text", "")
                    confidence = summary_field.get("ValueDetection", {}).get(
                        "Confidence", 0.0
                    )

                    extracted_fields.append(
                        ExtractedField(
                            name=field_type,
                            value=field_text,
                            confidence=confidence,
                            raw_text=field_text,
                        )
                    )

                    if "merchant" in field_type or "vendor" in field_type:
                        receipt_data.merchant_name = field_text
                    elif "date" in field_type:
                        receipt_data.transaction_date = field_text
                    elif "total" in field_type:
                        try:
                            receipt_data.total_amount = float(
                                field_text.replace("$", "").replace(",", "")
                            )
                        except:
                            pass
                    elif "tax" in field_type:
                        try:
                            receipt_data.tax_amount = float(
                                field_text.replace("$", "").replace(",", "")
                            )
                        except:
                            pass

        receipt_data.extracted_fields = extracted_fields
        receipt_data.items = items

        if extracted_fields:
            receipt_data.confidence_score = sum(
                f.confidence for f in extracted_fields
            ) / len(extracted_fields)

        return receipt_data

    @staticmethod
    def create_expense_record(
        invoice_data: InvoiceData, document_type: str = "invoice"
    ) -> ExpenseRecord:
        """Create ExpenseRecord from InvoiceData."""
        line_items = []
        for item in invoice_data.line_items:
            line_items.append(
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total": item.total_price,
                }
            )

        return ExpenseRecord(
            document_type=document_type,
            vendor=invoice_data.vendor_name,
            date=invoice_data.invoice_date,
            total=invoice_data.total_amount,
            currency="USD",
            line_items=line_items,
            metadata={
                "invoice_number": invoice_data.invoice_number,
                "tax_amount": invoice_data.tax_amount,
                "subtotal": invoice_data.subtotal,
            },
            confidence=invoice_data.confidence_score,
        )
