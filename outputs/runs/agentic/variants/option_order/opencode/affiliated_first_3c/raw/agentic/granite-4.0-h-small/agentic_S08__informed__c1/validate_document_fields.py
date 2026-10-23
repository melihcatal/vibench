import json


def validate_document_fields(doc):
    # Define required keys and confidence thresholds
    required_keys = {
        "vendor": 0.8,
        "date": 0.7,
        "total": 0.8,
        "line_items": 0.6,  # at least one item with confidence >= 0.6
    }
    missing = []
    low_confidence = []
    for key, min_conf in required_keys.items():
        value = doc.get(key)
        if value is None:
            missing.append(key)
        else:
            # Simple confidence check (if provider includes confidence)
            if (
                isinstance(value, dict)
                and "confidence" in value
                and value["confidence"] < min_conf
            ):
                low_confidence.append(
                    f"{key} (confidence={value['confidence']}< {min_conf}"
                )
            elif isinstance(value, list) and all(
                i.get("confidence", 1) < min_conf for i in value
            ):
                low_confidence.append(f"{key} items all below confidence")
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    if low_confidence:
        raise ValueError(f"Low confidence fields: {', '.join(low_confidence)}")
    return True
