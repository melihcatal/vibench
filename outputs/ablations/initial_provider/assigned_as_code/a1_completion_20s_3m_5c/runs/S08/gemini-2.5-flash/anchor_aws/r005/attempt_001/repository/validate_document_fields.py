from typing import Dict, Any, List
from document_models import DocumentExtractionResponse, ValidationRule, DocumentValidationConfig
from document_client import get_firestore_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_document_fields(extracted_data: Dict[str, Any], document_type: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    db = get_firestore_client()
    validation_config_ref = db.collection("validation_configs").document(document_type)
    validation_config_dict = validation_config_ref.get().to_dict()

    if not validation_config_dict:
        logger.warning(f"No validation configuration found for document type: {document_type}. Skipping validation.")
        return {"is_valid": True, "messages": ["No validation rules applied"], "validated_data": extracted_data}

    validation_config = DocumentValidationConfig(**validation_config_dict)

    is_valid = True
    messages = []
    
    # Convert extracted_data to DocumentExtractionResponse model for easier access and type checking
    # Note: This assumes extracted_data aligns with the DocumentExtractionResponse structure for confidence checks
    # We might need a more flexible way to access fields for validation, or a common structure.
    # For now, let's assume extracted_data directly contains fields like 'vendor', 'total', etc., with 'value' and 'confidence'.

    for rule in validation_config.rules:
        field_name = rule.field_name
        
        # Accessing nested fields from the extracted_data, assuming it's a dict of dicts (e.g., {'vendor': {'value': '...', 'confidence': ...}})
        field_data = extracted_data.get(field_name)

        if rule.required and (field_data is None or field_data.get("value") is None or field_data.get("value") == ""):
            is_valid = False
            messages.append(f"Required field '{field_name}' is missing or empty.")
        
        if field_data and field_data.get("confidence") is not None and field_data.get("confidence") < rule.min_confidence:
            is_valid = False
            messages.append(f"Confidence for field '{field_name}' ({field_data.get('confidence'):.2f}) is below minimum required confidence ({rule.min_confidence:.2f}).")

        # Optional: Add data type validation here based on rule.data_type
        if field_data and field_data.get("value") is not None and rule.data_type:
            field_value = field_data.get("value")
            if rule.data_type == "number":
                try:
                    float(field_value)
                except (ValueError, TypeError):
                    is_valid = False
                    messages.append(f"Field '{field_name}' has invalid data type. Expected {rule.data_type}, got {type(field_value).__name__} with value '{field_value}'.")
            # Add other data type validations (date, string etc.)

    return {"is_valid": is_valid, "messages": messages, "validated_data": extracted_data}
