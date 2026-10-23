from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional
import json


@dataclass
class CloudWatchLogEvent:
    timestamp: int
    message: str


def log_event_to_cloudwatch(event: Dict[str, Any]) -> CloudWatchLogEvent:
    ts = int(datetime.utcnow().timestamp() * 1000)
    msg = json.dumps(event)
    return CloudWatchLogEvent(ts, msg)


def cloudwatch_result_to_dict(result: Dict) -> List[Dict[str, Any]]:
    logs = []
    for row in result.get("results", []):
        log = {k: v for k, v in row.items() if k != "@ptr"}
        if "@message" in log:
            try:
                log["parsed"] = json.loads(log["@message"])
            except json.JSONDecodeError:
                pass
        logs.append(log)
    return logs


class QueryParams:
    start_time: int
    end_time: int
    query: str

    def __init__(self, start_time: int, end_time: int, query: str):
        self.start_time = start_time
        self.end_time = end_time
        self.query = query
