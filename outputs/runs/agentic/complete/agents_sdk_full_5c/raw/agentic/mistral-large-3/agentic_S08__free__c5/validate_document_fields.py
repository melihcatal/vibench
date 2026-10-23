from typing import Dict, Any, Union
from pydantic import ValidationError, BaseModel
from document_models import InvoiceFields, ReceiptFields, ValidationResult


def validate_document_fields(extracted_data: Union[InvoiceFields, ReceiptFields], confidence_threshold: float = 0.8) -> Dict[str, Any]:
    validation_result = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": []
    }

    try:
        if isinstance(extracted_data, InvoiceFields):
            model = InvoiceFields(**extracted_data.dict())
            required_fields = {
                "vendor": model.vendor,
                "date": model.date,
                "total": model.total
            }
            
            for field, value in required_fields.items():
                if not value:
                    validation_result["missing_fields"].append(field)
                elif hasattr(model, "confidence") and model.confidence.get(field, 1.0) < confidence_threshold:
                    validation_result["low_confidence_fields"].append(field)
                    
        elif isinstance(extracted_data, ReceiptFields):
            model = ReceiptFields(**extracted_data.dict())
            required_fields = {
                "merchant": model.merchant,
                "total": model.total
            }
            
            for field, value in required_fields.items():
                if not value:
                    validation_result["missing_fields"].append(field)
                elif hasattr(model, "confidence") and model.confidence.get(field, 1.0) < confidence_threshold:
                    validation_result["low_confidence_fields"].append(field)
                    
        if validation_result["missing_fields"] or validation_result["low_confidence_fields"]:
            validation_result["is_valid"] = False
            
    except ValidationError as e:
        validation_result["is_valid"] = False
        validation_result["validation_errors"] = str(e)

    return ValidationResult(**validation_result).dict()