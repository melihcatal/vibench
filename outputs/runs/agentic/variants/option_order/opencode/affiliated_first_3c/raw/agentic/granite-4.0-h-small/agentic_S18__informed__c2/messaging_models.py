import json
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Standardized request/response shapes for the same-scenario messaging flow
# ---------------------------------------------------------------------------

# Pub/Sub publishing request shape
PublishRequest = Dict[str, Any]

# Normalized event payload expected by downstream services
Event = Dict[str, Any]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def normalize_event(raw_payload: Dict[str, Any]) -> Event:
    """Convert arbitrary JSON payload into a canonical Event model.

    The canonical model includes only whitelisted top‑level fields and nests
    the original data under the 'data' key. This makes downstream consumers
    more resilient to schema evolution.

    Args:
        raw_payload (dict): Unstructured JSON received from an upstream producer.
    Returns:
        dict: Normalized event with guaranteed fields.
    """
    # Define required fields; missing ones become None
    normalized: Event = {
        "event_id": raw_payload.get("id", None),
        "type": raw_payload.get("type", None),
        "timestamp": raw_payload.get("timestamp", None),
        # All other arbitrary data is stored under 'data' to keep a fixed shape
        "data": {
            k: v for k, v in raw_payload.items() if k not in ("id", "type", "timestamp")
        },
    }
    return normalized


# ---------------------------------------------------------------------------
# Example usage (for local testing)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample = {
        "id": "order-123",
        "type": "order_created",
        "timestamp": "2025-08-15T12:34:56Z",
        "order_number": "ORD-001",
        "amount": 250.0,
    }
    print("Original:", sample)
    print("Normalized:", normalize_event(sample))
