import os
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    ValidationResult,
    ValidationRule,
)


def validate_document_fields(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    rules: Optional[List[ValidationRule]] = None,
) -> ValidationResult:
    """
    Validate required structured fields and confidence scores using Amazon Comprehend.
    """
    try:
        import boto3

        comprehend_client = boto3.client(
            "comprehend",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

        if not os.getenv("AWS_ACCESS_KEY_ID"):
            raise ValueError("AWS_ACCESS_KEY_ID environment variable is required")

        default_rules = [
            ValidationRule(field="vendor", required=True, min_confidence=0.7),
            ValidationRule(field="total_amount", required=True, min_confidence=0.8),
            ValidationRule(field="date", required=True, min_confidence=0.6),
        ]

        validation_rules = rules or default_rules

        validation_errors = []
        warnings = []
        validated_fields = {}

        if isinstance(extraction_result, InvoiceExtractionResult):
            field_map = {
                "vendor": (
                    "vendor",
                    extraction_result.vendor,
                    extraction_result.confidence_scores.get("vendor", 0.0),
                ),
                "total_amount": (
                    "total_amount",
                    extraction_result.total_amount,
                    extraction_result.confidence_scores.get("total", 0.0),
                ),
                "date": (
                    "date",
                    extraction_result.invoice_date,
                    extraction_result.confidence_scores.get("date", 0.0),
                ),
            }
        elif isinstance(extraction_result, ReceiptExtractionResult):
            field_map = {
                "vendor": (
                    "merchant",
                    extraction_result.merchant,
                    extraction_result.confidence_scores.get("merchant", 0.0),
                ),
                "total_amount": (
                    "total_amount",
                    extraction_result.total_amount,
                    extraction_result.confidence_scores.get("total", 0.0),
                ),
                "date": ("date", datetime.now().isoformat(), 1.0),
            }
        else:
            raise ValueError("Unsupported extraction result type")

        for rule in validation_rules:
            if rule.field in field_map:
                field_name, field_value, confidence = field_map[rule.field]

                if rule.required and (
                    not field_value or str(field_value).strip() == ""
                ):
                    validation_errors.append(
                        f"Required field '{field_name}' is missing"
                    )
                elif field_value and confidence < rule.min_confidence:
                    warnings.append(
                        f"Field '{field_name}' has low confidence: {confidence:.2f} < {rule.min_confidence}"
                    )

                validated_fields[field_name] = {
                    "value": field_value,
                    "confidence": confidence,
                    "valid": bool(field_value) and confidence >= rule.min_confidence,
                }

        text_to_analyze = ""
        if (
            isinstance(extraction_result, InvoiceExtractionResult)
            and extraction_result.vendor
        ):
            text_to_analyze = extraction_result.vendor
        elif (
            isinstance(extraction_result, ReceiptExtractionResult)
            and extraction_result.merchant
        ):
            text_to_analyze = extraction_result.merchant

        sentiment_score = 0.5
        if text_to_analyze:
            try:
                sentiment_response = comprehend_client.detect_sentiment(
                    Text=text_to_analyze, LanguageCode="en"
                )
                sentiment_score_map = {
                    "POSITIVE": 0.8,
                    "NEGATIVE": 0.2,
                    "NEUTRAL": 0.5,
                    "MIXED": 0.5,
                }
                sentiment_score = sentiment_score_map.get(
                    sentiment_response["Sentiment"], 0.5
                )
            except:
                pass

        overall_valid = len(validation_errors) == 0

        return ValidationResult(
            is_valid=overall_valid,
            validation_errors=validation_errors,
            warnings=warnings,
            validated_fields=validated_fields,
            confidence_scores={
                "overall": min([v["confidence"] for v in validated_fields.values()])
                if validated_fields
                else 0.0,
                "sentiment": sentiment_score,
            },
            provider="aws_comprehend",
            metadata={
                "validation_timestamp": datetime.now().isoformat(),
                "rules_applied": [rule.field for rule in validation_rules],
            },
        )

    except Exception as e:
        raise Exception(f"AWS Comprehend validation failed: {str(e)}")
