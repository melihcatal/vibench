# validate_document_fields.py
# [SAME-SCENARIO]
# Validates required structured fields and confidence scores from extracted documents.

import json
from typing import Dict, Any


def validate_fields(extracted: Dict[str, Any], required_fields: List[str]) -> bool:
    """Check that all required fields exist and have non-empty values.

    Args:
        extracted: Dictionary returned from an extraction step.
        required_fields: List of keys that must be present and truthy.

    Returns:
        True if validation passes, False otherwise.
    """
    missing = [f for f in required_fields if not extracted.get(f)]
    if missing:
        print(f"Validation failed: missing fields {missing}")
        return False
    # Simple confidence placeholder check (if scores are provided)
    if "confidence_scores" in extracted:
        low_conf = [k for k, v in extracted["confidence_scores"].items() if v < 0.5]
        if low_conf:
            print(f"Potential low confidence in fields: {low_conf}")
    return True


# Helper to return required fields for each scenario
def get_required_fields(scenario: str) -> List[str]:
    if scenario == "invoice":
        return ["vendor", "date", "total", "line_items"]
    elif scenario == "receipt":
        return ["merchant", "total", "items"]
    raise ValueError("Unsupported scenario")


# Example usage
if __name__ == "__main__":
    sample_invoice = {
        "vendor": "Acme Inc.",
        "date": "2024-05-10",
        "total": 250.0,
        "line_items": ["Widgets - 100.0", "Gadgets - 150.0"],
        "confidence_scores": {
            "vendor": 0.95,
            "date": 0.9,
            "total": 0.85,
            "line_items": 0.9,
        },
    }
    required = get_required_fields("invoice")
    is_valid = validate_fields(sample_invoice, required)
    print(json.dumps(is_valid, indent=2))
