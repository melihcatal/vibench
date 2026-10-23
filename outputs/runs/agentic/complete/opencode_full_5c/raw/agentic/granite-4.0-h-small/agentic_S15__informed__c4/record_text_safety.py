import json
from typing import Dict, Any
from database_models import DocumentRequest, SafetyCheckResponse, SafetyCheckRequest
from database_client import client


def check_text_safety(request: DocumentRequest) -> Dict[str, Any]:
    """
    Scans all user‑provided text fields in a document for unsafe content.
    Delegates to the chosen Content Safety service via safe_check().
    Returns a dict summarising which fields were flagged and any reasons.
    """
    raw = request["data"]  # user payload
n    safety_reqs: List[SafetyCheckRequest] = []

    # Simple heuristic: text values, column strings, or array of strings
    for field, value in raw.items():
        if isinstance(value, str):
            safety_reqs.append(SafetyCheckRequest(text=value))
        elif isinstance(value, list) and all(isinstance(i, str) for i in value):
            for txt in value:
                safety_reqs.append(SafetyCheckRequest(text=txt))

    flags = []
    for req in safety_reqs:
        resp = safe_check(req)
        if not resp.safe:
            flags.append({
                "field": req,  # placeholder – in real code we'd know the field name
                "reason": resp.flagged_reason
            })
    return {
        "safe": len(flags) == 0,
        "flags": flags
    }

# Placeholder for the actual provider client (Anthropic, Azure, etc.)
def safe_check(req: SafetyCheckRequest) -> SafetyCheckResponse:
    # In production replace with an SDK/REST call to the selected service
    # Here we demonstrate returning a dummy safe result.
    return SafetyCheckResponse(safe=True, flagged_reason="")

# Demo usage
if __name__ == "__main__":
    demo_doc = {
        "id": "demo-002",
        "data": {
            "title": "Safe Title",
            "note": "All fine here.",
            "comments": ["Nice", "Great job"]
        }
    }
    result = check_text_safety(DocumentRequest(**demo_doc))
    print(json.dumps(result, indent=2))