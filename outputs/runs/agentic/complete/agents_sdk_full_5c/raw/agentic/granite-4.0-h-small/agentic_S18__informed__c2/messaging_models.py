from typing import TypedDict, Dict

class PubSubPayload(TypedDict):
    """Normalized payload shape that downstream services expect."""
    event_id: str
    body: str
    timestamp: float
    source: str

    # Additional optional keys can be added as needed
    extra: Dict[str, str] = {}

def normalize_payload(raw_payload: dict) -> PubSubPayload:
    """Convert a raw JSON dict into the standardized PubSubPayload model."""
    # Ensure required fields are present; otherwise raise for downstream handling
    try:
        event_id = str(raw_payload["event_id"]) if "event_id" in raw_payload else str(uuid.uuid4())
        body = str(raw_payload.get("body", ""))
        # Use incoming timestamp if present, otherwise current Unix epoch
        timestamp = float(raw_payload.get("timestamp", str(time.time())))
        source = raw_payload.get("source", "unknown")
    except Exception as exc:
        raise ValueError("Invalid event payload structure") from exc
    return PubSubPayload(event_id=event_id, body=body, timestamp=timestamp, source=source, extra=dict(raw_payload))

class ProcessingResult(TypedDict):
    """Result of a processing step (e.g., translation, moderation)."""
    status: str  # e.g., \"ok\", \"failed\", \"dead_letter\"
    message_id: str
    reason: str | None = None
    transformed_payload: dict | None = None

    # Additional fields can be attached per use‑case
    dlq_topic: str | None = None

def build_processing_result(message_id: str, status: str, reason: str | None = None) -> ProcessingResult:
    return ProcessingResult(status=status, message_id=message_id, reason=reason)
