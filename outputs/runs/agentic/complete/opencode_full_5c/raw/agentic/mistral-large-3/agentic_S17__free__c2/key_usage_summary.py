from security_models import KeyUsageEvent
from typing import List, Dict
import json
import datetime


def summarize_key_usage(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = {}
    for event in events:
        key_id = event["key_id"]
        operation = event["operation"]
        status = event["status"]
        if key_id not in summary:
            summary[key_id] = {
                "encrypt": {"success": 0, "failure": 0},
                "decrypt": {"success": 0, "failure": 0},
                "sign": {"success": 0, "failure": 0},
                "verify": {"success": 0, "failure": 0},
            }
        if operation in summary[key_id]:
            summary[key_id][operation][status] += 1
    return summary
