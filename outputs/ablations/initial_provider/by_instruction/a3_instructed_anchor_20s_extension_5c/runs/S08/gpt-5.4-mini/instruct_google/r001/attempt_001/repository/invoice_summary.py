from typing import Any, Dict

from google.cloud import aiplatform


def invoice_summary(fields: Dict[str, Any]) -> str:
    aiplatform.init()
    vendor = fields.get("vendor") or fields.get("merchant") or "unknown"
    total = fields.get("total")
    return f"Invoice from {vendor} totaling {total}"
