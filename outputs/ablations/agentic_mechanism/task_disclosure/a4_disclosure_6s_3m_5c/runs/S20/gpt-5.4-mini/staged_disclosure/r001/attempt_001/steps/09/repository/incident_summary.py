import argparse
import json
import os
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Optional

import requests


GRAFANA_LOKI_QUERY_RANGE_URL = "https://logs-prod-us.grafana.net/loki/api/v1/query_range"


@dataclass(frozen=True)
class ErrorSummary:
    total_logs: int
    error_logs: int
    top_messages: list[tuple[str, int]]
    top_services: list[tuple[str, int]]
    first_seen: Optional[str]
    last_seen: Optional[str]


def _parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _to_ns(dt: datetime) -> int:
    return int(dt.timestamp() * 1_000_000_000)


def _extract_timestamp(value: Any) -> Optional[str]:
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
    return None


def _extract_labels(stream: dict[str, Any]) -> dict[str, str]:
    labels = stream.get("stream") or {}
    return {str(key): str(val) for key, val in labels.items()}


def _message_from_line(line: str) -> str:
    text = line.strip()
    if not text:
        return ""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(payload, dict):
        for key in ("message", "msg", "error", "log", "event"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return json.dumps(payload, sort_keys=True)
    return text


def _service_from_labels(labels: dict[str, str]) -> str:
    for key in ("service", "app", "job", "component", "name"):
        value = labels.get(key)
        if value:
            return value
    return "unknown"


def _is_error(labels: dict[str, str], line: str) -> bool:
    severity = labels.get("severity", "").lower()
    level = labels.get("level", "").lower()
    line_lower = line.lower()
    return any(token in {severity, level} for token in {"error", "err", "fatal", "panic"}) or "error" in line_lower or "exception" in line_lower or "traceback" in line_lower


def fetch_error_logs(start: str, end: str, limit: int = 1000) -> list[dict[str, Any]]:
    username = os.environ.get("GRAFANA_CLOUD_LOGS_USERNAME")
    token = os.environ.get("GRAFANA_CLOUD_API_KEY")
    if not username or not token:
        raise RuntimeError("GRAFANA_CLOUD_LOGS_USERNAME and GRAFANA_CLOUD_API_KEY are required")
    params = {
        "query": '{severity=~"error|fatal|panic|err"} |= ""',
        "start": _to_ns(_parse_time(start)),
        "end": _to_ns(_parse_time(end)),
        "limit": limit,
    }
    response = requests.get(GRAFANA_LOKI_QUERY_RANGE_URL, params=params, auth=(username, token), timeout=30)
    response.raise_for_status()
    data = response.json()
    logs: list[dict[str, Any]] = []
    for stream in data.get("data", {}).get("result", []):
        labels = _extract_labels(stream)
        for ts, line in stream.get("values", []):
            logs.append({"timestamp": _extract_timestamp(ts), "labels": labels, "line": line})
    return logs


def summarize_errors(logs: Iterable[dict[str, Any]]) -> ErrorSummary:
    total_logs = 0
    error_logs = 0
    message_counts: Counter[str] = Counter()
    service_counts: Counter[str] = Counter()
    timestamps: list[str] = []
    for entry in logs:
        total_logs += 1
        labels = entry.get("labels") or {}
        line = str(entry.get("line") or "")
        if not _is_error(labels, line):
            continue
        error_logs += 1
        message = _message_from_line(line) or line.strip() or "(empty message)"
        service = _service_from_labels(labels)
        message_counts[message] += 1
        service_counts[service] += 1
        timestamp = entry.get("timestamp")
        if isinstance(timestamp, str) and timestamp:
            timestamps.append(timestamp)
    first_seen = min(timestamps) if timestamps else None
    last_seen = max(timestamps) if timestamps else None
    return ErrorSummary(
        total_logs=total_logs,
        error_logs=error_logs,
        top_messages=message_counts.most_common(5),
        top_services=service_counts.most_common(5),
        first_seen=first_seen,
        last_seen=last_seen,
    )


def format_summary(summary: ErrorSummary) -> str:
    lines = [
        f"total_logs={summary.total_logs}",
        f"error_logs={summary.error_logs}",
        f"first_seen={summary.first_seen or 'n/a'}",
        f"last_seen={summary.last_seen or 'n/a'}",
        "top_services=" + ", ".join(f"{service}:{count}" for service, count in summary.top_services) if summary.top_services else "top_services=n/a",
        "top_messages=" + ", ".join(f"{message}:{count}" for message, count in summary.top_messages) if summary.top_messages else "top_messages=n/a",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=False)
    parser.add_argument("--end", required=False)
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()
    if args.start and args.end:
        logs = fetch_error_logs(args.start, args.end, args.limit)
        print(format_summary(summarize_errors(logs)))
    else:
        print("Provide --start and --end to fetch and summarize incident errors.")


if __name__ == "__main__":
    main()
