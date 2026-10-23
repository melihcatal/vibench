import boto3
from typing import Dict, Any, Optional
from security_models import PayloadScanRequest, PayloadScanResponse


def check_payload_safety(request: PayloadScanRequest, region_name: str) -> PayloadScanResponse:
    client = boto3.client("comprehend", region_name=region_name)

    # Amazon Comprehend can be used for detecting PII, sentiment, entities, etc.
    # For content moderation, a common approach is to combine entity detection with custom classifiers
    # or use external services if Comprehend's built-in capabilities are not sufficient.
    # For this exercise, we will demonstrate PII detection as a proxy for "unsafe content".
    # A real-world content moderation system would be more complex and might involve multiple services.

    is_safe = True
    findings = {}

    # Detect PII (Personally Identifiable Information)
    try:
        pii_response = client.detect_pii_entities(Text=request.payload_text, LanguageCode="en")
        if pii_response["Entities"]:
            is_safe = False
            findings["pii_entities"] = pii_response["Entities"]
    except Exception as e:
        # Handle cases where text might be too long or other Comprehend errors
        findings["error_pii_detection"] = str(e)

    # You could extend this with other Comprehend features like sentiment analysis, custom entity recognition,
    # or integrate with other services for more advanced content moderation.

    return PayloadScanResponse(
        is_safe=is_safe,
        findings=findings
    )
