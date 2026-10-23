import json
from typing import List, Dict


def summarize(results: List[Dict]) -> Dict[str, int]:
    """Aggregate processing results into a simple summary."""
    summary = {
        "total_processed": len(results),
        "success": 0,
        "dead_lettered": 0,
        "failed_validation": 0,
    }
    for r in results:
        if r.get("status") == "dead_letter":
            summary["dead_lettered"] += 1
        elif r.get("status") == "failed_validation":
            summary["failed_validation"] += 1
        else:
            summary["success"] += 1
    return summary
