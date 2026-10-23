import json
import os
from typing import Any, Dict, List, Optional

import requests


class GrafanaLokiClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.base_url = (base_url or os.getenv("GRAFANA_LOKI_URL") or "https://logs-prod-006.grafana.net").rstrip("/")
        self.api_key = api_key or os.getenv("GRAFANA_LOKI_API_KEY") or os.getenv("GRAFANA_CLOUD_API_KEY")
        if not self.api_key:
            raise ValueError("Missing Grafana Loki API key")

    def write_correlated_logs(
        self,
        messages: List[str],
        request_id: str,
        stream_labels: Optional[Dict[str, str]] = None,
        timestamp_ns: Optional[int] = None,
    ) -> Dict[str, Any]:
        labels = {"service": "application", "request_id": request_id}
        if stream_labels:
            labels.update(stream_labels)

        entries = []
        for index, message in enumerate(messages):
            entry_ts = timestamp_ns if timestamp_ns is not None else self._now_ns()
            payload = {
                "request_id": request_id,
                "correlation_id": request_id,
                "sequence": index,
                "message": message,
            }
            entries.append([str(entry_ts), json.dumps(payload, separators=(",", ":"))])

        url = f"{self.base_url}/loki/api/v1/push"
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"streams": [{"stream": labels, "values": entries}]},
            timeout=30,
        )
        response.raise_for_status()
        return {"status_code": response.status_code, "request_id": request_id, "written": len(entries)}

    @staticmethod
    def _now_ns() -> int:
        return int(__import__("time").time() * 1_000_000_000)


def write_correlated_logs(messages: List[str], request_id: str, stream_labels: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    client = GrafanaLokiClient()
    return client.write_correlated_logs(messages=messages, request_id=request_id, stream_labels=stream_labels)
