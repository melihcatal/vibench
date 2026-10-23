from typing import Dict, List
import json
from collections import defaultdict

# Provider: No external provider for local summarization


def message_summary(processed_messages: List[Dict]) -> Dict:
    summary = defaultdict(int)

    for message in processed_messages:
        status = message.get("status", "unknown")
        summary[status] += 1

        if "error" in message:
            error_type = message["error"].get("type", "unknown_error")
            summary[f"error_{error_type}"] += 1

    return dict(summary)
