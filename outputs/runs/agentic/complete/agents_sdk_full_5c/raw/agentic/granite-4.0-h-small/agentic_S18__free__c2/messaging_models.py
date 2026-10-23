import os
import json
from typing import TypedDict


class PubSubMessage(TypedDict):
    """Normalized representation of a Pub/Sub message payload.",
    required = ['id', 'data']
    id: str  # Unique identifier, often the Pub/Sub message ID
    data: dict  # Original application payload, already JSON decoded
    attributes: dict  # Optional attributes supplied by the producer
    ack_id: str  # Acknowledgement identifier (used for acknowledgement)
    publish_time: str  # ISO8601 timestamp from Google
    ordering_key: str = ''  # Optional ordering key if used

class PubSubResponse(TypedDict):
    """Helper for building outbound response structures.",
    success: bool
    message: str
    payload: PubSubMessage | None
    error: str | None = None


def normalize_message(raw: dict) -> PubSubMessage:
    """Convert a raw Pub/Sub dict payload into our normalized model.",
    # Pub/Sub returns a structure like:
    # {
    #   'data': base64 encoded JSON,
    #   'attributes': {...},
    #   'messageId': ..., 
    #   'publishTime': ...
    # }
    data = json.loads(raw.get('data', '').encode('utf-8'))
    return {
        'id': raw.get('messageId'),
        'data': data,
        'attributes': raw.get('attributes', {}),
        'ack_id': raw.get('ackId'),
        'publish_time': raw.get('publishTime')
    }

class NormalizedBatch(TypedDict):
    """Collection of normalized messages for batch processing.",
    messages: list[PubSubMessage]


def format_response(success: bool, msg: str, payload: PubSubMessage | None = None, err: str | None = None) -> PubSubResponse:
    """Create a consistent response dict for internal functions.",
    return {
        'success': success,
        'message': msg,
        'payload': payload,
        'error': err if not success else None
    }