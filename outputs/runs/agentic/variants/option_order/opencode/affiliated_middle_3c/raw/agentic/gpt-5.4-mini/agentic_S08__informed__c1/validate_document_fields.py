from document_client import as_dict


def validate_document_fields(payload):
    data = as_dict(payload)
    required = ["vendor", "date", "total"]
    missing = [name for name in required if not data.get(name)]
    confidence = (
        data.get("confidence", {})
        if isinstance(data.get("confidence", {}), dict)
        else {}
    )
    low_confidence = [
        k for k, v in confidence.items() if isinstance(v, (int, float)) and v < 0.8
    ]
    return {
        "valid": not missing and not low_confidence,
        "missing": missing,
        "low_confidence": low_confidence,
    }
