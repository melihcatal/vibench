# messaging_models.py
# LOCAL HELPER: shared request/response structures and normalization utilities for Pub/Sub integration

from typing import TypedDict, Dict, Any, List
from datetime import datetime

# Normalized representation of an incoming Pub/Sub message payload
class NormalizedMessage(TypedDict):
    event_type: str
    event_id: str
    payload: Dict[str, Any]
    received_at: datetime

# Validation helpers

def validate_event_schema(event: dict) -> bool:
    """Very simple schema check for required keys."""
    required = {"event_type", "event_id", "payload"}
    return required.issubset(event.keys())

# Payload normalizer (converts raw JSON to the internal model)
def normalize_message(raw: dict) -> NormalizedMessage:
    """Transform raw JSON payload into a strongly typed model."""
    if not validate_event_schema(raw):
        raise ValueError("Missing required event fields")
    return {
        "event_type": raw["event_type"],
        "event_id": raw["event_id"],
        "payload": raw.get("payload", {}),
        "received_at": datetime.utcnow(),
    }

# Example of how to use the model elsewhere:
# def handle_message(raw_json: str) -> None:
#     try:
#         msg: NormalizedMessage = normalize_message(json.loads(raw_json))
#         print("Processing", msg[\"event_type\"], \"with ID\", msg[\"event_id\"])\n#     except Exception as exc:
#         print(\"Invalid message\", exc)
