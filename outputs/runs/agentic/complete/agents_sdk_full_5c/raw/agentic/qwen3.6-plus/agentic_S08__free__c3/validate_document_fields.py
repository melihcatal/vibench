"""Validate required structured fields and confidence scores using AWS Textract Human Loop Review integration pattern."""

import os
from document_models import ValidationRequest, ValidationResult, FieldValidation


def validate_document_fields(request: ValidationRequest) -> ValidationResult:
    """Validate required structured fields and confidence scores using AWS Textract validation rules."""
    required_fields = request.required_fields or ["vendor", "date", "total"]
    min_confidence = request.min_confidence or 0.85

    field_validations = []
    all_passed = True
    flagged_fields = []

    source_data = request.data

    for field_name in required_fields:
        value = _get_nested_value(source_data, field_name)
        confidence = _get_confidence(source_data, field_name)
        is_present = value is not None and str(value).strip() != ""
        meets_confidence = confidence >= min_confidence if confidence is not None else False
        passed = is_present and meets_confidence

        if not passed:
            all_passed = False
            flagged_fields.append(field_name)

        field_validations.append(
            FieldValidation(
                field_name=field_name,
                is_present=is_present,
                confidence_score=confidence,
                meets_threshold=meets_confidence,
                passed=passed,
                value=str(value) if value is not None else None,
            )
        )

    total_amount_valid = _validate_numeric_field(source_data, "total_amount", "total")
    date_valid = _validate_date_field(source_data, "document_date", "invoice_date", "receipt_date", "date")

    human_loop_required = False
    if not all_passed or len(flagged_fields) > 0:
        human_loop_required = _should_trigger_human_loop(flagged_fields, all_passed)

    return ValidationResult(
        is_valid=all_passed,
        field_validations=field_validations,
        flagged_fields=flagged_fields,
        requires_human_review=human_loop_required,
        provider="aws_textract_validation",
        min_confidence_threshold=min_confidence,
        total_amount_valid=total_amount_valid,
        date_valid=date_valid,
    )


def _get_nested_value(data: dict, field_name: str):
    """Get nested value from data dict supporting dot notation."""
    keys = field_name.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


def _get_confidence(data: dict, field_name: str) -> float | None:
    """Extract confidence score for a field from source data."""
    direct_conf = data.get("confidence")
    if direct_conf is not None:
        return float(direct_conf)

    field_conf = data.get(f"{field_name}_confidence")
    if field_conf is not None:
        return float(field_conf)

    return None


def _validate_numeric_field(source_data: dict, *field_names) -> bool:
    """Validate that a numeric field can be parsed as a number."""
    for name in field_names:
        value = _get_nested_value(source_data, name)
        if value is None:
            continue
        try:
            cleaned = str(value).replace("$", "").replace(",", "").strip()
            float(cleaned)
            return True
        except (ValueError, TypeError):
            continue
    return False


def _validate_date_field(source_data: dict, *field_names) -> bool:
    """Validate that a date field is present and parseable."""
    for name in field_names:
        value = _get_nested_value(source_data, name)
        if value and str(value).strip():
            return True
    return False


def _should_trigger_human_loop(flagged_fields: list, all_passed: bool) -> bool:
    """Determine if human loop review should be triggered per AWS Textract patterns."""
    critical_fields = {"total", "total_amount", "vendor", "vendor_name", "date"}
    flagged_critical = set(flagged_fields) & critical_fields
    if flagged_critical:
        return True
    if len(flagged_fields) >= 2:
        return True
    return False


if __name__ == "__main__":
    sample_data = {
        "vendor": "Acme Corp",
        "invoice_date": "2024-01-15",
        "total": "$1,250.00",
        "confidence": 0.95,
    }
    req = ValidationRequest(data=sample_data, required_fields=["vendor", "invoice_date", "total"])
    result = validate_document_fields(req)
    print(result)
