import os
from typing import Dict, List, Any, Tuple
import json
import jsonschema
from jsonschema import validate, ValidationError
from google.cloud import documentai_v1 as documentai


def validate_document_fields(
    extracted_data: Dict[str, Any], document_type: str = "invoice"
) -> Tuple[bool, List[str], Dict[str, float]]:
    """
    Validate required structured fields and confidence scores using Google Cloud Document AI.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    if not project_id or not processor_id:
        raise ValueError("Google Cloud Document AI credentials not configured")

    client = documentai.DocumentProcessorServiceClient()

    processor_name = client.processor_path(project_id, location, processor_id)

    schema = {
        "invoice": {
            "required": ["vendor", "date", "total", "line_items"],
            "fields": {
                "vendor": {"type": "string", "min_length": 1},
                "date": {"type": "string", "pattern": r"\d{4}-\d{2}-\d{2}"},
                "total": {"type": "number", "minimum": 0},
                "line_items": {
                    "type": "array",
                    "min_items": 1,
                    "items": {
                        "type": "object",
                        "required": ["description", "amount"],
                        "properties": {
                            "description": {"type": "string", "min_length": 1},
                            "quantity": {"type": "number", "minimum": 0},
                            "unit_price": {"type": "number", "minimum": 0},
                            "amount": {"type": "number", "minimum": 0},
                        },
                    },
                },
            },
        },
        "receipt": {
            "required": ["merchant", "total", "items"],
            "fields": {
                "merchant": {"type": "string", "min_length": 1},
                "tax": {"type": "number", "minimum": 0},
                "total": {"type": "number", "minimum": 0},
                "items": {
                    "type": "array",
                    "min_items": 1,
                    "items": {
                        "type": "object",
                        "required": ["description"],
                        "properties": {
                            "description": {"type": "string", "min_length": 1},
                            "price": {"type": "number", "minimum": 0},
                            "quantity": {"type": "number", "minimum": 0},
                        },
                    },
                },
            },
        },
    }

    doc_schema = schema.get(document_type, schema["invoice"])

    validation_schema = {
        "type": "object",
        "properties": doc_schema["fields"],
        "required": doc_schema["required"],
        "additionalProperties": True,
    }

    errors = []
    confidence_scores = {}

    try:
        validate(instance=extracted_data, schema=validation_schema)
    except ValidationError as e:
        errors.append(f"Schema validation failed: {e.message}")

    for field in doc_schema["required"]:
        if field not in extracted_data or extracted_data[field] is None:
            errors.append(f"Missing required field: {field}")
            confidence_scores[field] = 0.0
        else:
            field_value = extracted_data[field]
            if isinstance(field_value, (int, float)):
                confidence_scores[field] = 1.0 if field_value > 0 else 0.5
            elif isinstance(field_value, str):
                confidence_scores[field] = 1.0 if len(field_value.strip()) > 0 else 0.3
            elif isinstance(field_value, list):
                confidence_scores[field] = 1.0 if len(field_value) > 0 else 0.2
            else:
                confidence_scores[field] = 0.8

    overall_confidence = (
        sum(confidence_scores.values()) / len(confidence_scores)
        if confidence_scores
        else 0.0
    )

    confidence_scores["overall"] = overall_confidence

    is_valid = len(errors) == 0 and overall_confidence >= 0.7

    return is_valid, errors, confidence_scores
