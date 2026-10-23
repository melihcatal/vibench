import os
import boto3
from botocore.config import Config
from document_models import FieldValidation, ValidationResult


def validate_document_fields(
    extraction: dict, required_fields: list = None
) -> ValidationResult:
    if required_fields is None:
        required_fields = ["vendor_name", "invoice_date", "total_amount", "currency"]

    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    config = Config(
        region_name=aws_region,
        retries={"max_attempts": 3, "mode": "standard"},
    )

    textract_client = boto3.client(
        "textract",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=config,
    )

    field_results = []
    warnings = []
    all_valid = True

    for field_name in required_fields:
        value = extraction.get(field_name)
        confidence = extraction.get("confidence_scores", {}).get(field_name, 0.0)

        present = value is not None and value != "" and value != 0
        meets_threshold = confidence >= 0.7 if confidence > 0 else present

        if present and confidence < 0.7:
            warnings.append(
                f"Field '{field_name}' has low confidence: {confidence:.2f}"
            )

        is_valid = present and meets_threshold
        if not is_valid:
            all_valid = False

        message = ""
        if not present:
            message = f"Field '{field_name}' is missing"
        elif not meets_threshold:
            message = (
                f"Field '{field_name}' confidence {confidence:.2f} below threshold 0.7"
            )

        field_results.append(
            FieldValidation(
                field_name=field_name,
                present=present,
                confidence=confidence,
                valid=is_valid,
                message=message,
            )
        )

    validation_result = ValidationResult(
        is_valid=all_valid,
        field_results=field_results,
        warnings=warnings,
    )

    return validation_result
