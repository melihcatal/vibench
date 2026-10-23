from typing import Dict, List


def summarize_incident(logs: List[Dict[str, str]]) -> Dict[str, object]:
    errors = [item for item in logs if str(item.get("severity", "")).lower() == "error"]
    services = sorted({str(item.get("service", "unknown")) for item in errors})
    return {
        "error_count": len(errors),
        "services": services,
        "summary": f"Observed {len(errors)} error logs across {len(services)} services.",
    }
