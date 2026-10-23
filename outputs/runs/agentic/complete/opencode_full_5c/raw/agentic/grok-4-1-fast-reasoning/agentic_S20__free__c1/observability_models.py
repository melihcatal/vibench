from typing import List, Dict, Any, Optional
import json

LogEntry = Dict[str, str]


def extract_message(log_entry: LogEntry) -> str:
    return log_entry.get("@message", "")


def parse_structured_message(message: str) -> Dict[str, Any]:
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        return {"raw_message": message}


def logs_to_summary_text(logs: List[LogEntry]) -> str:
    lines = []
    for log in logs:
        ts = log.get("@timestamp", "")
        msg = log.get("@message", "")
        lines.append(f"[{ts}] {msg}")
    return "\n".join(lines)
