from __future__ import annotations

from typing import Any, Dict, Iterable, List

from messaging_client import load_config, send_batch_to_queue
from messaging_models import BatchPublishResult, build_envelope, normalize_message_payload


def batch_publish(items: Iterable[Dict[str, Any]]) -> BatchPublishResult:
    config = load_config()
    envelopes = []
    for item in items:
        envelopes.append(
            build_envelope(
                message_id=str(item.get("message_id", "")),
                payload=normalize_message_payload(item.get("payload", {})),
                attributes=item.get("attributes", {}),
                correlation_id=item.get("correlation_id"),
            )
        )
    published_ids = send_batch_to_queue(config.batch_target, envelopes, config=config)
    return BatchPublishResult(published_ids=published_ids, provider=config.provider, target=config.batch_target)
