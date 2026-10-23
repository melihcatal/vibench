from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError, validator
from document_models import ValidatedDocument


def validate_document_fields(
    extracted_data: Dict[str, Any],
    min_confidence: float = 0.8
) -> Optional[Dict[str, Any]]:
    """Validate required structured fields and confidence scores using Pydantic."""
    try:
        validated = ValidatedDocument(**extracted_data)
        
        # Check confidence scores if available
        if hasattr(validated, "confidence_scores"):
            for field, score in validated.confidence_scores.items():
                if score < min_confidence:
                    raise ValueError(f"Field {field} has low confidence score: {score}")
        
        return validated.dict()
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None