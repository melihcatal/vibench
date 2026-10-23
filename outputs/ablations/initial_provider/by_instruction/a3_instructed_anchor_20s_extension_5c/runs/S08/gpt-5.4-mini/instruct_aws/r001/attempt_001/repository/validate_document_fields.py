import boto3


def validate_document_fields(fields, confidences=None, minimum_confidence=0.8):
    required = ["vendor", "date", "total"]
    missing = [name for name in required if not fields.get(name)]
    low_confidence = []
    confidences = confidences or {}
    for name in required:
        if confidences.get(name, 1.0) < minimum_confidence:
            low_confidence.append(name)
    return {"valid": not missing and not low_confidence, "missing": missing, "low_confidence": low_confidence, "provider": "aws-textract"}
