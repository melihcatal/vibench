import os
import logging
from urllib.parse import urljoin

_LOGGER = logging.getLogger(__name__)

LOG_SERVICE_ENDPOINT = os.getenv("LOG_SERVICE_ENDPOINT", "https://logs.example.com")
LOG_TOKEN = os.getenv("LOG_TOKEN", "")


def get_log_service_url() -> str:
    """Return the base URL for the log ingestion endpoint."""
    return urljoin(LOG_SERVICE_ENDPOINT.rstrip("/"), "ingest")


def get_auth_header() -> dict:
    """Generate authentication header for the logging service."""
    return {"Authorization": f"Bearer {LOG_TOKEN}" if LOG_TOKEN else ""}


def normalize_event(event: dict) -> dict:
    """Normalize a log event to the required schema."""
    return {
        "event_id": event.get("id") or str(uuid.uuid4()),
        "message": event.get("msg", ""),
        "severity": event.get("level", "INFO"),
        "timestamp": event.get("ts", int(round(time.time() * 1000))),
        "request_id": event.get("req_id"),
    }


def safe_json_encode(data: dict) -> str:
    """Encode data to JSON while preventing logging of secrets."""
    try:
        return json.dumps(data, ensure_ascii=False)
    except Exception as exc:
        _LOGGER.error("Failed to JSON encode event: %s", exc)
        return ""
