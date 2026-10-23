import json
import re

def validate_document_fields(doc_json):
    """
    Validate a normalized expense document (output from normalize_expense) against required fields
    and confidence score expectations. Returns a tuple: (is_valid: bool, issues: List[str]).
    """
    required_keys = ["vendor_or_merchant", "total"]
    if doc_json.get("date"):
        required_keys.append("date")
    if doc_json.get("subtotal"):
        required_keys.append("subtotal")
    if doc_json.get("tax"):
        required_keys.append("tax")
    issues = []
    # Check presence of required keys
    for key in required_keys:
        if not doc_json.get(key):
            issues.append(f"Missing required field: {key}")
    # Validate that "total" is a non‑negative number
    total = doc_json.get("total")
    if total is None:
        issues.append("Total must be present and numeric."
    elif not isinstance(total, (int, float)) or total < 0:
        issues.append("Total must be a non‑negative number.")
    # Simple regex check for date format (YYYY‑MM‑DD optional)
    if doc_json.get("date"):
        if not re.match(r"\d{4}-\d{2}-\d{2}", doc_json["date"]):
            issues.append("Date format should be YYYY‑MM‑DD.")
    # If line_items exist, ensure at least description present
    for idx, li in enumerate(doc_json.get("line_items", [])):
        if "description" not in li:
            issues.append(f"Line‑item {idx} missing description.")
    confidence = doc_json.get("confidence")
    if confidence is not None and (not isinstance(confidence, float) or not (0 <= confidence <= 1)):
        issues.append("Confidence score must be a float between 0 and 1 when provided.")
    valid = len(issues) == 0
    return valid, issues
