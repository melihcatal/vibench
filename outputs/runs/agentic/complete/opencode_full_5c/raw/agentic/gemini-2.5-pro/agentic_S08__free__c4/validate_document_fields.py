import os
from typing import Dict
import boto3
from document_models import ValidationResult


def validate_document_fields(
    extracted_data: Dict, document_image: bytes
) -> ValidationResult:
    """
    Validates required structured fields and uses AWS Rekognition for image quality check.
    """
    errors = []
    confidence_scores = {}

    required_fields = ["vendor_name", "invoice_date", "total_amount"]
    for field in required_fields:
        if field not in extracted_data or not extracted_data[field]:
            errors.append(f"Missing required field: {field}")

        # Simple confidence simulation
        confidence_scores[field] = extracted_data.get(f"{field}_confidence", 0.95)

    # AWS Rekognition for image quality check as a proxy for document confidence
    rekognition_client = boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        response = rekognition_client.detect_text(Image={"Bytes": document_image})
        text_detections = response.get("TextDetections", [])
        if not text_detections:
            errors.append("Low document quality: No text detected by AWS Rekognition.")
            confidence_scores["document_quality"] = 0.1
        else:
            # Average confidence of detected text as a quality score
            avg_confidence = (
                sum(d["Confidence"] for d in text_detections)
                / len(text_detections)
                / 100
            )
            confidence_scores["document_quality"] = avg_confidence
            if avg_confidence < 0.7:
                errors.append(
                    "Low document quality: Average text confidence below threshold."
                )
    except Exception as e:
        errors.append(f"AWS Rekognition check failed: {str(e)}")
        confidence_scores["document_quality"] = 0.0

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        confidence_scores=confidence_scores,
    )
