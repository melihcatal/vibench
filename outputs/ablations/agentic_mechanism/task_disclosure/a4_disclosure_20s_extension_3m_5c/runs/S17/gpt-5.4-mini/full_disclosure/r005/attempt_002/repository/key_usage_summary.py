import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class OpenAIKeyUsageSummaryClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, method=method)
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def list_key_events(self, limit: int = 100, after: Optional[str] = None) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"limit": limit}
        if after:
            params["after"] = after
        data = self._request("GET", "/organization/usage/keys", params)
        return data.get("data", []) if isinstance(data, dict) else []

    def list_audit_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        data = self._request("GET", "/organization/audit_logs", {"limit": limit})
        return data.get("data", []) if isinstance(data, dict) else []


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_timestamp(value: Any) -> str:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    if isinstance(value, str):
        return value
    return _iso_now()


def summarize_key_usage(key_events: List[Dict[str, Any]], audit_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    per_key: Dict[str, Dict[str, Any]] = {}
    total_requests = 0
    total_tokens = 0
    error_events = 0

    for event in key_events:
        key_id = str(event.get("key_id") or event.get("key") or event.get("id") or "unknown")
        item = per_key.setdefault(key_id, {"requests": 0, "tokens": 0, "last_seen": None})
        item["requests"] += int(event.get("requests", event.get("count", 1)) or 1)
        item["tokens"] += int(event.get("tokens", event.get("usage", 0)) or 0)
        ts = _normalize_timestamp(event.get("created_at") or event.get("timestamp") or event.get("time"))
        if item["last_seen"] is None or ts > item["last_seen"]:
            item["last_seen"] = ts
        total_requests += int(event.get("requests", event.get("count", 1)) or 1)
        total_tokens += int(event.get("tokens", event.get("usage", 0)) or 0)
        if event.get("status") in {"error", "failed"}:
            error_events += 1

    notable_events = []
    for event in audit_events:
        action = event.get("action") or event.get("type") or "unknown"
        if action in {"key.created", "key.updated", "key.deleted", "api_key.rotated", "api_key.revoked"}:
            notable_events.append({
                "action": action,
                "actor": event.get("actor") or event.get("user") or event.get("username") or "unknown",
                "target": event.get("target") or event.get("key_id") or event.get("resource") or "unknown",
                "timestamp": _normalize_timestamp(event.get("created_at") or event.get("timestamp") or event.get("time")),
            })

    top_keys = sorted(per_key.items(), key=lambda kv: (kv[1]["requests"], kv[1]["tokens"]), reverse=True)
    return {
        "provider": "openai",
        "generated_at": _iso_now(),
        "summary": {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "error_events": error_events,
            "distinct_keys": len(per_key),
        },
        "top_keys": [
            {"key_id": key_id, **stats}
            for key_id, stats in top_keys[:10]
        ],
        "notable_crypto_events": notable_events[:50],
    }


def main() -> None:
    client = OpenAIKeyUsageSummaryClient()
    key_events = client.list_key_events()
    audit_events = client.list_audit_events()
    print(json.dumps(summarize_key_usage(key_events, audit_events), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
