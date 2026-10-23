"""
Validate required structured fields and confidence scores using Amazon Bedrock.
Provider: Amazon Bedrock (Claude 3 Sonnet model for validation reasoning)
"""

import os
import json
import re
from typing import Dict, Any, List, Optional, Tuple
import boto3
from botocore.exceptions import ClientError

from document_models import ValidationRequest, ValidationResponse, FieldValidation


def validate_document_fields(
    extracted_data: Dict[str, Any],
    required_fields: Optional[List[str]] = None,
    min_confidence: float = 0.70,
    aws_region: Optional[str] = None,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
) -> ValidationResponse:
    """
    Validate that extracted document fields meet structural requirements and confidence thresholds.
    
    Uses Amazon Bedrock with Claude 3 Sonnet to perform intelligent field validation:
    - Checks required fields are present
    - Validates confidence scores meet minimum threshold
    - Performs semantic validation (e.g., date formats, numeric ranges)
    - Returns per-field validation results with explanations
    
    Args:
        extracted_data: Dictionary of extracted fields with values and confidence scores
        required_fields: List of field names that must be present
        min_confidence: Minimum acceptable confidence score (0.0-1.0)
        aws_region: AWS region for Bedrock
        model_id: Bedrock model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)
    
    Returns:
        ValidationResponse with per-field validation results
    """
    region = aws_region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    default_required = required_fields or [
        "vendor",
        "date",
        "total_amount",
    ]
    
    field_validations = _perform_schema_validation(extracted_data, default_required, min_confidence)
    
    if not all(fv.is_valid for fv in field_validations):
        llm_validation = _invoke_bedrock_validation(
            bedrock_client,
            extracted_data,
            default_required,
            min_confidence,
            field_validations,
            model_id,
        )
        if llm_validation:
            field_validations = _merge_validations(field_validations, llm_validation)
    
    overall_valid = all(fv.is_valid for fv in field_validations)
    
    return ValidationResponse(
        is_valid=overall_valid,
        fields=field_validations,
        required_fields=default_required,
        min_confidence=min_confidence,
    )


def _perform_schema_validation(
    data: Dict[str, Any],
    required_fields: List[str],
    min_confidence: float,
) -> List[FieldValidation]:
    """Perform basic schema-level validation on extracted fields."""
    validations: List[FieldValidation] = []
    
    for field_name in required_fields:
        value = data.get(field_name)
        confidence = data.get(f"{field_name}_confidence", data.get("confidence", 1.0))
        
        if value is None or (isinstance(value, str) and value.strip() == ""):
            validations.append(
                FieldValidation(
                    field_name=field_name,
                    is_valid=False,
                    confidence=confidence,
                    error="Missing required field",
                )
            )
        elif confidence < min_confidence:
            validations.append(
                FieldValidation(
                    field_name=field_name,
                    is_valid=False,
                    confidence=confidence,
                    error=f"Confidence {confidence:.2f} below threshold {min_confidence}",
                )
            )
        else:
            type_error = _validate_field_type(field_name, value)
            validations.append(
                FieldValidation(
                    field_name=field_name,
                    is_valid=type_error is None,
                    confidence=confidence,
                    error=type_error,
                )
            )
    
    for field_name, value in data.items():
        if field_name not in required_fields and not field_name.endswith("_confidence"):
            confidence = data.get(f"{field_name}_confidence", data.get("confidence", 1.0))
            if value is not None and not (isinstance(value, str) and value.strip() == ""):
                type_error = _validate_field_type(field_name, value)
                validations.append(
                    FieldValidation(
                        field_name=field_name,
                        is_valid=type_error is None,
                        confidence=confidence,
                        error=type_error,
                    )
                )
    
    return validations


def _validate_field_type(field_name: str, value: Any) -> Optional[str]:
    """Validate field value matches expected type based on field name."""
    lower_name = field_name.lower()
    
    if "date" in lower_name:
        if not _is_valid_date(str(value)):
            return f"Invalid date format: {value}"
    
    if "amount" in lower_name or "total" in lower_name or "tax" in lower_name or "price" in lower_name:
        if isinstance(value, str):
            try:
                float(value.replace("$", "").replace(",", "").strip())
            except (ValueError, TypeError):
                return f"Invalid numeric value: {value}"
    
    if "vendor" in lower_name or "merchant" in lower_name:
        if isinstance(value, str) and len(value.strip()) < 2:
            return "Vendor name too short"
    
    return None


def _is_valid_date(date_str: str) -> bool:
    """Check if a string looks like a valid date."""
    date_patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}-\d{2}-\d{4}",
        r"\w+ \d{1,2},? \d{4}",
        r"\d{1,2} \w+ \d{4}",
    ]
    for pattern in date_patterns:
        if re.match(pattern, date_str.strip()):
            return True
    return False


def _invoke_bedrock_validation(
    client: Any,
    extracted_data: Dict[str, Any],
    required_fields: List[str],
    min_confidence: float,
    field_validations: List[FieldValidation],
    model_id: str,
) -> Optional[List[Dict[str, Any]]]:
    """Use Amazon Bedrock Claude model to perform additional validation reasoning."""
    failed_fields = [fv for fv in field_validations if not fv.is_valid]
    
    if not failed_fields:
        return None
    
    prompt = f"""You are a document extraction validation assistant. Review the following extracted fields and their validation status.

Required fields: {', '.join(required_fields)}
Minimum confidence threshold: {min_confidence}

Extracted data:
{json.dumps(extracted_data, indent=2, default=str)}

Field validations that failed:
{json.dumps([{"field": fv.field_name, "error": fv.error, "confidence": fv.confidence} for fv in failed_fields], indent=2)}

For each failed field, determine if the data is actually acceptable despite the initial failure. 
Return a JSON array with objects containing: field_name, is_valid (true/false), and reason (string explanation).
Only return the JSON array, no other text."""
    
    try:
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            }),
        )
        
        response_body = json.loads(response["body"].read())
        content = response_body.get("content", [{}])[0].get("text", "")
        
        json_match = re.search(r"\[.*\]", content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except ClientError as e:
        print(f"Bedrock validation failed: {e}")
    
    return None


def _merge_validations(
    original: List[FieldValidation],
    llm_results: List[Dict[str, Any]],
) -> List[FieldValidation]:
    """Merge LLM validation results with original validations."""
    merged = []
    
    for fv in original:
        for llm_result in llm_results:
            if llm_result.get("field_name") == fv.field_name or llm_result.get("field") == fv.field_name:
                new_is_valid = llm_result.get("is_valid", fv.is_valid)
                new_error = llm_result.get("reason") or fv.error
                merged.append(
                    FieldValidation(
                        field_name=fv.field_name,
                        is_valid=new_is_valid,
                        confidence=fv.confidence,
                        error=None if new_is_valid else new_error,
                    )
                )
                break
        else:
            merged.append(fv)
    
    return merged


if __name__ == "__main__":
    sample = {
        "vendor": "ABC Corporation",
        "vendor_confidence": 0.95,
        "date": "2024-01-15",
        "date_confidence": 0.88,
        "total_amount": 125.50,
        "total_amount_confidence": 0.92,
        "line_items": [],
    }
    
    result = validate_document_fields(sample)
    print(result.model_dump_json(indent=2))
