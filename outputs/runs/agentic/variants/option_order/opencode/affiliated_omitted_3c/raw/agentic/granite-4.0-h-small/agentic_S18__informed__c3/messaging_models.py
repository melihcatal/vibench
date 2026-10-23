from typing import Any, Dict, List

class Event:
    """Model representing a single Pub/Sub event payload.",
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.id: Optional[str] = None  # set by client after publish

class BatchResult:
    """Container for results of a batch publish operation.",
    def __init__(self, message_ids: List[str]):
        self.message_ids = message_ids

class PullResponse:
    """Container for a single pulled message.",
    def __init__(self, data: Dict[str, Any], ack_id: str):
        self.data = data
        self.ack_id = ack_id

class DeadLetterPayload:
    """Representation of a message moved to a dead‑letter topic.",
    def __init__(self, source_subscription: str, original_id: str, payload: Dict[str, Any]):
        self.source_subscription = source_subscription
        self.original_id = original_id
        self.payload = payload
