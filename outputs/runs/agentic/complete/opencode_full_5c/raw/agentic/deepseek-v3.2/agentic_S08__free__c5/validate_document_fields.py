import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from document_models import ValidationResult


def validate_document_fields(
    extracted_data: Dict[str, Any],
    required_fields: List[str] = None,
    min_confidence: float = 0.7,
) -> Dict[str, Any]:
    """
    Validate required structured fields and confidence scores using Amazon Textract.
    """
    import boto3
    from botocore.exceptions import ClientError

    # Initialize Textract client
    textract_client = boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    if required_fields is None:
        required_fields = ["vendor", "date", "total"]

    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "field_details": {},
        "validation_timestamp": None,
    }

    # Check for missing fields
    for field in required_fields:
        if field not in extracted_data or extracted_data[field] is None:
            validation_results["missing_fields"].append(field)
            validation_results["is_valid"] = False

    # Simulate confidence checking (in real scenario, this would come from Textract response)
    # For demonstration, we'll check if we have confidence scores in the data
    if "confidence_scores" in extracted_data:
        confidence_data = extracted_data["confidence_scores"]
        for field, confidence in confidence_data.items():
            if confidence < min_confidence:
                validation_results["low_confidence_fields"].append(
                    {
                        "field": field,
                        "confidence": confidence,
                        "threshold": min_confidence,
                    }
                )
                validation_results["is_valid"] = False

    # Add field details
    for field, value in extracted_data.items():
        if field != "confidence_scores":
            validation_results["field_details"][field] = {
                "value": value,
                "type": type(value).__name__,
                "is_present": value is not None,
            }

    # Use Textract to analyze document structure (simplified example)
    try:
        # In a real implementation, you would call Textract analyze_document
        # For this example, we'll simulate validation
        document_structure_valid = True

        # Check if total is numeric if present
        if "total" in extracted_data and extracted_data["total"] is not None:
            try:
                float(str(extracted_data["total"]).replace("$", "").replace(",", ""))
            except ValueError:
                validation_results["field_details"]["total"]["validation_note"] = (
                    "Total is not a valid number"
                )
                document_structure_valid = False

        validation_results["document_structure_valid"] = document_structure_valid

    except ClientError as e:
        validation_results["textract_error"] = str(e)
        validation_results["is_valid"] = False

    # Add timestamp
    from datetime import datetime

    validation_results["validation_timestamp"] = datetime.utcnow().isoformat()

    return validation_results


def validate_with_confidence_scores(
    extracted_data: Dict[str, Any],
    confidence_scores: Dict[str, float],
    min_confidence: float = 0.7,
) -> Tuple[bool, List[str]]:
    """
    Validate fields based on confidence scores.
    """
    low_confidence_fields = []

    for field, confidence in confidence_scores.items():
        if confidence < min_confidence:
            low_confidence_fields.append(field)

    is_valid = len(low_confidence_fields) == 0

    return is_valid, low_confidence_fields


if __name__ == "__main__":
    # Example usage
    sample_data = {
        "vendor": "ABC Corp",
        "date": "2024-01-15",
        "total": 1250.75,
        "line_items": [
            {"description": "Item 1", "amount": 1000},
            {"description": "Item 2", "amount": 250.75},
        ],
        "confidence_scores": {
            "vendor": 0.85,
            "date": 0.92,
            "total": 0.78,
            "line_items": 0.65,
        },
    }

    result = validate_document_fields(sample_data)
    print(json.dumps(result, indent=2))
