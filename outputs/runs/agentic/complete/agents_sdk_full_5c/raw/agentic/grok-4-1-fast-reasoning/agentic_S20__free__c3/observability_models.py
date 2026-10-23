from dataclasses import dataclass, asdict
from typing import Dict, Any, List
import json
from datetime import datetime

@dataclass
class StructuredLog:
    level: str
    message: str
    service: str
    correlation_id: str | None = None

def to_cloudwatch_event(log: StructuredLog, timestamp_ms: int | None = None) -> Dict[str, Any]:
    if timestamp_ms is None:
        timestamp_ms = int(datetime.now().timestamp() * 1000)
    message_json = json.dumps(asdict(log))
    return {
        "timestamp": timestamp_ms,
        "message": message_json
    }

def parse_query_row(row: List[Dict[str, str]]) -> Dict[str, str]:
    log = {}
    for field in row:
        log[field['field']] = field['value']
    return log
