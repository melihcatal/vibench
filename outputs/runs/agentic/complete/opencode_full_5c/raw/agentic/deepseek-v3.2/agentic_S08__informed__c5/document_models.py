from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class ExpenseField:
    """Represents a single extracted field from a document."""

    field_type: str
    value: Any
    confidence: float
    label: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_type": self.field_type,
            "value": self.value,
            "confidence": self.confidence,
            "label": self.label,
        }


@dataclass
class LineItem:
    """Represents a line item from an invoice or receipt."""

    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "confidence": self.confidence,
        }


@dataclass
class DocumentExtraction:
    """Container for extracted document data."""

    vendor: Optional[ExpenseField] = None
    merchant: Optional[ExpenseField] = None
    date: Optional[ExpenseField] = None
    total: Optional[ExpenseField] = None
    tax: Optional[ExpenseField] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None

    def to_normalized_json(self) -> Dict[str, Any]:
        """Convert to normalized JSON schema."""
        return {
            "vendor": self.vendor.to_dict() if self.vendor else None,
            "merchant": self.merchant.to_dict() if self.merchant else None,
            "date": self.date.to_dict() if self.date else None,
            "total": self.total.to_dict() if self.total else None,
            "tax": self.tax.to_dict() if self.tax else None,
            "line_items": [item.to_dict() for item in self.line_items],
            "extraction_timestamp": datetime.utcnow().isoformat(),
        }


def parse_textract_expense_response(response: Dict[str, Any]) -> DocumentExtraction:
    """Parse Amazon Textract AnalyzeExpense response."""
    extraction = DocumentExtraction(raw_response=response)

    for expense_doc in response.get("ExpenseDocuments", []):
        for field in expense_doc.get("SummaryFields", []):
            field_type = field.get("Type", {}).get("Text", "").lower()
            value_text = field.get("ValueDetection", {}).get("Text", "")
            confidence = field.get("ValueDetection", {}).get("Confidence", 0.0) / 100.0

            expense_field = ExpenseField(
                field_type=field_type, value=value_text, confidence=confidence
            )

            if "vendor" in field_type:
                extraction.vendor = expense_field
            elif "merchant" in field_type:
                extraction.merchant = expense_field
            elif "date" in field_type:
                extraction.date = expense_field
            elif "total" in field_type:
                extraction.total = expense_field
            elif "tax" in field_type:
                extraction.tax = expense_field

        for line_item_group in expense_doc.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                line_item_data = {}
                for field in line_item.get("LineItemExpenseFields", []):
                    field_type = field.get("Type", {}).get("Text", "").lower()
                    value_text = field.get("ValueDetection", {}).get("Text", "")

                    if "description" in field_type:
                        line_item_data["description"] = value_text
                    elif "quantity" in field_type:
                        try:
                            line_item_data["quantity"] = float(value_text)
                        except (ValueError, TypeError):
                            line_item_data["quantity"] = None
                    elif "unit" in field_type and "price" in field_type:
                        try:
                            line_item_data["unit_price"] = float(
                                value_text.replace("$", "").replace(",", "")
                            )
                        except (ValueError, TypeError):
                            line_item_data["unit_price"] = None
                    elif "total" in field_type and "price" in field_type:
                        try:
                            line_item_data["total_price"] = float(
                                value_text.replace("$", "").replace(",", "")
                            )
                        except (ValueError, TypeError):
                            line_item_data["total_price"] = None

                if "description" in line_item_data:
                    extraction.line_items.append(
                        LineItem(
                            description=line_item_data.get("description", ""),
                            quantity=line_item_data.get("quantity"),
                            unit_price=line_item_data.get("unit_price"),
                            total_price=line_item_data.get("total_price"),
                            confidence=0.9,
                        )
                    )

    return extraction
