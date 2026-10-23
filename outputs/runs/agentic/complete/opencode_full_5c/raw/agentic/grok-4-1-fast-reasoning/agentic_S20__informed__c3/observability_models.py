import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List


@dataclass
class StructuredLog:
    timestamp: int
    level: str
    message: str
    service: str = "unknown"
    correlation_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


def log_to_aws_event(log: StructuredLog) -> dict:
    payload = asdict(log)
    payload.pop("timestamp")
    return {"timestamp": log.timestamp, "message": json.dumps(payload)}


def aws_event_to_structured_log(event: dict) -> StructuredLog:
    payload = {}
    if "message" in event:
        try:
            payload = json.loads(event["message"])
        except json.JSONDecodeError:
            payload = {"message": event["message"], "level": "INFO"}
    return StructuredLog(
        timestamp=event["timestamp"],
        message=payload.get("message", ""),
        level=payload.get("level", "INFO"),
        service=payload.get("service", "unknown"),
        correlation_id=payload.get("correlation_id"),
        data=payload.get("data"),
    )
