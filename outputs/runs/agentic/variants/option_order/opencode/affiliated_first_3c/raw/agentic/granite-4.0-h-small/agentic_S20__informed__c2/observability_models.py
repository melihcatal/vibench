# [HELPER] observability_models.py
"""Define local request, response, and normalization helpers for Managed Log Query / Log Ingestion."""

from typing import Dict, Any, Optional


class LogRequest:
    """Representation of a structured log payload.

    Attributes:
        timestamp (str): ISO8601 UTC timestamp.
        severity (str): Log severity level.
        message (str): Human‑readable message.
        correlation_id (Optional[str]): Optional request or trace ID.
        additional (Dict[str, Any]): Arbitrary extra fields.
    """

    def __init__(
        self,
        message: str,
        severity: str = "info",
        correlation_id: Optional[str] = None,
        **additional: Any,
    ):
        self.timestamp = self._utc_now()
        self.severity = severity
        self.message = message
        self.correlation_id = correlation_id
        self.additional = additional

    @staticmethod
    def _utc_now() -> str:
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z"

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.additional:
            payload["extra"] = self.additional
        return payload


class LogResponse:
    """Normalization wrapper for log query responses.

    Different providers may return different shapes; this normalizes them to a list of dicts.
    """

    def __init__(self, raw: Any):
        self.raw = raw
        self.events = self._normalize(raw)

    def _normalize(self, raw: Any) -> list[Dict[str, Any]]:
        # Example normalization for IBM Cloud Logs (REST) response
        if hasattr(raw, "json") and callable(raw.json):
            data = raw.json()
            # Assume array under 'logs' key
            return data.get("logs", [])
        # Example normalization for Alibaba SDK response (PutLogs)
        if isinstance(raw, dict) and "logGroupList" in raw:
            return [log["contents"] for log in raw.get("logGroupList", [])]
        # Example normalization for AWS CloudWatch (filter_log_events)
        if isinstance(raw, dict) and "events" in raw:
            return raw.get("events", [])
        # Fallback: try to iterate if it looks iterable
        try:
            return [e for e in raw]
        except TypeError:
            return []

    def as_list(self) -> list[Dict[str, Any]]:
        return self.events


class LogEmbeddingRequest:
    """Wrapper for sending selected log messages to an embedding model.

    The provider field indicates which later‑step service to use.
    """

    def __init__(
        self,
        provider: str,
        messages: list[str],
        model_id: Optional[str] = None,
    ):
        self.provider = provider
        self.messages = messages
        self.model_id = model_id or "default"

    def to_payload(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model_id": self.model_id,
            "messages": self.messages,
        }


class LogEmbeddingResult:
    """Placeholder for embeddings returned from a model.

    In production this would contain vector data, token counts, etc.
    """

    def __init__(self, embeddings: list[Dict[str, Any]]):
        self.embeddings = embeddings

    def as_json(self) -> str:
        import json

        return json.dumps(self.embeddings, ensure_ascii=False)
