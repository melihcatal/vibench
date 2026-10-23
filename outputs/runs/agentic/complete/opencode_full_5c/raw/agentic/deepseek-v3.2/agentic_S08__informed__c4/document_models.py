from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class ExtractionField:
    name: str
    value: Any
    confidence: Optional[float] = None
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "confidence": self.confidence,
            "source": self.source,
        }


@dataclass
class DocumentExtraction:
    document_id: str
    document_type: str
    provider: str
    fields: List[ExtractionField]
    overall_confidence: Optional[float] = None
    extraction_timestamp: datetime = field(default_factory=datetime.utcnow)
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "document_type": self.document_type,
            "provider": self.provider,
            "fields": [field.to_dict() for field in self.fields],
            "overall_confidence": self.overall_confidence,
            "extraction_timestamp": self.extraction_timestamp.isoformat() + "Z",
            "raw_response": self.raw_response,
        }

    def get_field(self, field_name: str) -> Optional[ExtractionField]:
        for field in self.fields:
            if field.name == field_name:
                return field
        return None

    def get_field_value(self, field_name: str) -> Any:
        field = self.get_field(field_name)
        return field.value if field else None


@dataclass
class NormalizedExpense:
    expense_id: str
    source_document_id: str
    source_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence_score: Optional[float] = None
    normalized_timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "expense_id": self.expense_id,
            "source_document_id": self.source_document_id,
            "source_type": self.source_type,
            "vendor": self.vendor,
            "merchant": self.merchant,
            "date": self.date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "line_items": self.line_items,
            "metadata": self.metadata,
            "confidence_score": self.confidence_score,
            "normalized_timestamp": self.normalized_timestamp.isoformat() + "Z",
        }

    @classmethod
    def from_extraction(cls, extraction: DocumentExtraction) -> "NormalizedExpense":
        expense = cls(
            expense_id=f"exp_{extraction.document_id}",
            source_document_id=extraction.document_id,
            source_type=extraction.document_type,
        )

        if extraction.document_type == "invoice":
            expense.vendor = extraction.get_field_value("VendorName")
            expense.date = extraction.get_field_value("InvoiceDate")
            expense.total_amount = extraction.get_field_value("InvoiceTotal")

            items_field = extraction.get_field("Items")
            if items_field and items_field.value:
                expense.line_items = cls._normalize_invoice_items(items_field.value)

        elif extraction.document_type == "receipt":
            expense.merchant = extraction.get_field_value("merchant_name")
            expense.total_amount = extraction.get_field_value("total_amount")
            expense.tax_amount = extraction.get_field_value("tax")

            items_field = extraction.get_field("line_items")
            if items_field and items_field.value:
                expense.line_items = cls._normalize_receipt_items(items_field.value)

        expense.confidence_score = extraction.overall_confidence
        expense.metadata = {
            "extraction_provider": extraction.provider,
            "extraction_timestamp": extraction.extraction_timestamp.isoformat() + "Z",
        }

        return expense

    @staticmethod
    def _normalize_invoice_items(items_data: Any) -> List[Dict[str, Any]]:
        normalized_items = []

        if isinstance(items_data, list):
            for item in items_data:
                if isinstance(item, dict):
                    normalized_item = {
                        "description": item.get("Description"),
                        "quantity": item.get("Quantity"),
                        "unit_price": item.get("UnitPrice"),
                        "amount": item.get("Amount"),
                        "category": None,
                    }
                    normalized_items.append(normalized_item)

        return normalized_items

    @staticmethod
    def _normalize_receipt_items(items_data: Any) -> List[Dict[str, Any]]:
        normalized_items = []

        if isinstance(items_data, list):
            for item in items_data:
                if isinstance(item, dict):
                    normalized_item = {
                        "description": item.get("description"),
                        "quantity": item.get("quantity"),
                        "unit_price": item.get("unit_price"),
                        "total_amount": item.get("total_amount"),
                        "category": None,
                    }
                    normalized_items.append(normalized_item)

        return normalized_items


@dataclass
class ValidationResult:
    document_id: str
    is_valid: bool
    missing_fields: List[str]
    low_confidence_fields: List[str]
    field_validations: Dict[str, Dict[str, Any]]
    overall_confidence: Optional[float] = None
    validation_timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "is_valid": self.is_valid,
            "missing_fields": self.missing_fields,
            "low_confidence_fields": self.low_confidence_fields,
            "field_validations": self.field_validations,
            "overall_confidence": self.overall_confidence,
            "validation_timestamp": self.validation_timestamp.isoformat() + "Z",
        }

    @property
    def validation_score(self) -> float:
        total_fields = len(self.field_validations)
        if total_fields == 0:
            return 0.0

        valid_fields = sum(
            1
            for validation in self.field_validations.values()
            if validation.get("valid", False)
        )

        return valid_fields / total_fields


class DocumentModelFactory:
    @staticmethod
    def create_extraction_from_azure(
        response: Any, document_type: str, document_id: str
    ) -> DocumentExtraction:
        fields = []

        for field_name, field in response.documents[0].fields.items():
            field_value = None
            if hasattr(field, "value_string") and field.value_string:
                field_value = field.value_string
            elif hasattr(field, "value_number") and field.value_number:
                field_value = field.value_number
            elif hasattr(field, "value_date") and field.value_date:
                field_value = field.value_date

            confidence = field.confidence if hasattr(field, "confidence") else None

            fields.append(
                ExtractionField(
                    name=field_name,
                    value=field_value,
                    confidence=confidence,
                    source="azure",
                )
            )

        overall_confidence = (
            response.documents[0].confidence
            if hasattr(response.documents[0], "confidence")
            else None
        )

        return DocumentExtraction(
            document_id=document_id,
            document_type=document_type,
            provider="azure",
            fields=fields,
            overall_confidence=overall_confidence,
            raw_response=json.loads(json.dumps(response.as_dict()))
            if hasattr(response, "as_dict")
            else None,
        )

    @staticmethod
    def create_extraction_from_mindee(
        response: Any, document_type: str, document_id: str
    ) -> DocumentExtraction:
        fields = []
        document = response.document

        for attr_name in dir(document):
            if not attr_name.startswith("_"):
                attr = getattr(document, attr_name)
                if hasattr(attr, "value") and attr.value is not None:
                    fields.append(
                        ExtractionField(
                            name=attr_name,
                            value=attr.value,
                            confidence=attr.confidence
                            if hasattr(attr, "confidence")
                            else None,
                            source="mindee",
                        )
                    )

        overall_confidence = (
            document.inference.confidence
            if hasattr(document.inference, "confidence")
            else None
        )

        return DocumentExtraction(
            document_id=document_id,
            document_type=document_type,
            provider="mindee",
            fields=fields,
            overall_confidence=overall_confidence,
        )
