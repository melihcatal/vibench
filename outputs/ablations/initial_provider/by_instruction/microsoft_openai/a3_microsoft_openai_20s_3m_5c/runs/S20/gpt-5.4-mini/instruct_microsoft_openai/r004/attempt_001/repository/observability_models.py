from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_severity(severity: Optional[str]) -> str:
    if not severity:
        return "INFO"
    return severity.strip().upper()


def normalize_log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(event)
    normalized["severity"] = normalize_severity(event.get("severity"))
    if "message" in normalized and normalized["message"] is None:
        normalized["message"] = ""
    return normalized


@dataclass
class LogWriteResponse:
    ok: bool
    id: Optional[str]
    raw: Dict[str, Any]


@dataclass
class LogQueryResponse:
    ok: bool
    results: List[Dict[str, Any]]
    raw: Dict[str, Any]


def extract_results(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(response.get("data"), list):
        return response["data"]
    if isinstance(response.get("results"), list):
        return response["results"]
    if isinstance(response.get("items"), list):
        return response["items"]
    return []
