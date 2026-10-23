from typing import Dict, Any, Tuple
from pydantic import ValidationError
from document_models import ExpenseSchema

class DocumentValidator:
    def __init__(self, min_confidence: float = 0.7):
        self.min_confidence = min_confidence

    def validate(self, extracted_data: Dict[str, Any], source_type: str) -> Tuple[bool, Dict[str, Any]]:
        try:
            if source_type == "invoice":
                normalized = ExpenseSchema(**{
                    "source_type": "invoice",
                    "vendor": extracted_data.get("vendor", ""),
                    "date": extracted_data.get("date"),
                    "total_amount": extracted_data.get("total"),
                    "line_items": extracted_data.get("line_items", []),
                    "currency": "USD",
                    "confidence": extracted_data.get("confidence", 0.0),
                    "metadata": {"original_fields": extracted_data}
                })
            elif source_type == "receipt":
                normalized = ExpenseSchema(**{
                    "source_type": "receipt",
                    "vendor": extracted_data.get("merchant", ""),
                    "total_amount": extracted_data.get("total"),
                    "line_items": extracted_data.get("items", []),
                    "tax_amount": extracted_data.get("tax"),
                    "currency": "USD",
                    "confidence": extracted_data.get("confidence", 0.0),
                    "metadata": {"original_fields": extracted_data}
                })
            else:
                return False, {"error": "Unsupported source type"}

            if normalized.confidence < self.min_confidence:
                return False, {"error": "Confidence below threshold", "confidence": normalized.confidence}

            return True, {"normalized_data": normalized.dict()}

        except ValidationError as e:
            return False, {"error": "Validation failed", "details": str(e)}

    def check_required_fields(self, extracted_data: Dict[str, Any], source_type: str) -> Tuple[bool, list]:
        missing_fields = []
        if source_type == "invoice":
            if not extracted_data.get("vendor"):
                missing_fields.append("vendor")
            if not extracted_data.get("total"):
                missing_fields.append("total")
            if not extracted_data.get("line_items"):
                missing_fields.append("line_items")
        elif source_type == "receipt":
            if not extracted_data.get("merchant"):
                missing_fields.append("merchant")
            if not extracted_data.get("total"):
                missing_fields.append("total")
            if not extracted_data.get("items"):
                missing_fields.append("items")

        return len(missing_fields) == 0, missing_fields