from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import ValidationIssue


PROVIDER = "Azure Document Intelligence"
MIN_CONFIDENCE = 0.5
DOCUMENT_INTELLIGENCE_CLIENT = DocumentIntelligenceClient


def validate_document_fields(extracted_payload: dict) -> dict:
    fields = extracted_payload.get("extracted_fields", extracted_payload)
    issues = []

    required = ["total"]
    if "vendor" in fields or extracted_payload.get("model_id") == "prebuilt-invoice":
        required.extend(["vendor", "date", "line_items"])
    if "merchant" in fields or extracted_payload.get("model_id") == "prebuilt-receipt":
        required.extend(["merchant", "tax", "items"])

    for key in required:
        value = fields.get(key)
        if value in (None, "", []):
            issues.append(ValidationIssue(field=key, message="Missing required field").to_dict())
            continue
        if isinstance(value, dict):
            confidence = value.get("confidence")
            if confidence is not None and confidence < MIN_CONFIDENCE:
                issues.append(
                    ValidationIssue(
                        field=key,
                        message=f"Confidence below threshold: {confidence}",
                        severity="warning",
                    ).to_dict()
                )
        if isinstance(value, list):
            for idx, item in enumerate(value):
                confidence = item.get("confidence") if isinstance(item, dict) else None
                if confidence is not None and confidence < MIN_CONFIDENCE:
                    issues.append(
                        ValidationIssue(
                            field=f"{key}[{idx}]",
                            message=f"Line confidence below threshold: {confidence}",
                            severity="warning",
                        ).to_dict()
                    )

    return {
        "provider": PROVIDER,
        "valid": not any(issue["severity"] == "error" for issue in issues),
        "issues": issues,
    }
