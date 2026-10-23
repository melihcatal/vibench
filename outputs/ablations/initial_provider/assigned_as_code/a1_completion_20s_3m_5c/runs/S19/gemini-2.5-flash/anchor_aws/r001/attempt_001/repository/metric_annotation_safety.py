import os
from typing import Dict, Any

import boto3

from observability_models import AnnotationSafetyCheckResult

def metric_annotation_safety(payload: Dict[str, Any], config: Dict[str, Any] = None) -> AnnotationSafetyCheckResult:
    region_name = config.get("region") if config else os.environ.get("AWS_REGION", "us-east-1")
    comprehend_client = boto3.client("comprehend", region_name=region_name)

    text_to_check = payload["annotation_text"]

    if not text_to_check:
        return AnnotationSafetyCheckResult(unsafe_content_found=False, details="No text to check.")

    try:
        # Detect PII entities in the text
        response = comprehend_client.detect_pii_entities(Text=text_to_check, LanguageCode=payload.get("language_code", "en"))

        unsafe_content_found = False
        details = []

        if response["Entities"]:
            unsafe_content_found = True
            for entity in response["Entities"]:
                details.append(f"Found {entity["Type"]} at offset {entity["BeginOffset"]}-{entity["EndOffset"]}: '')"

        if unsafe_content_found:
            return AnnotationSafetyCheckResult(unsafe_content_found=True, details="; ".join(details))
        else:
            return AnnotationSafetyCheckResult(unsafe_content_found=False, details="No unsafe content (PII) detected.")

    except Exception as e:
        return AnnotationSafetyCheckResult(unsafe_content_found=True, details=f"Error during safety check: {str(e)}")
