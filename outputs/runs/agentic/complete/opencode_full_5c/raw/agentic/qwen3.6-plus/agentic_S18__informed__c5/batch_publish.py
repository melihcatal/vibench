from typing import Optional
from messaging_models import EventMessage, BatchPublishResult, normalize_event_payload
from messaging_client import get_publisher_client, get_topic_path, ensure_topic_exists


def batch_publish(
    topic_name: str,
    events: list[dict],
    default_attributes: Optional[dict] = None,
) -> BatchPublishResult:
    ensure_topic_exists(topic_name)
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_name)
    results = []
    total_sent = 0
    total_failed = 0
    error_summary = None
    try:
        with publisher.batch() as batch:
            for idx, event_data in enumerate(events):
                normalized = normalize_event_payload(event_data.get("payload", {}))
                event = EventMessage(
                    event_id=event_data.get("event_id"),
                    event_type=event_data.get("event_type", "unknown"),
                    source=event_data.get("source", ""),
                    payload=normalized,
                    attributes={
                        **(default_attributes or {}),
                        **(event_data.get("attributes", {})),
                        "batch_index": str(idx),
                    },
                )
                data = event.to_json().encode("utf-8")
                pub_attrs = {k: str(v) for k, v in event.attributes.items()}
                future = batch.publish(topic_path, data, **pub_attrs)
                results.append(
                    {
                        "event_id": event.event_id,
                        "event_type": event.event_type,
                        "future": future,
                    }
                )
        for r in results:
            try:
                message_id = r["future"].result()
                r["message_id"] = message_id
                r["success"] = True
                total_sent += 1
            except Exception as e:
                r["success"] = False
                r["error"] = str(e)
                total_failed += 1
        success = total_failed == 0
        return BatchPublishResult(
            results=[
                {
                    "event_id": r["event_id"],
                    "event_type": r["event_type"],
                    "message_id": r.get("message_id", ""),
                    "success": r.get("success", False),
                    "error": r.get("error"),
                }
                for r in results
            ],
            total_sent=total_sent,
            total_failed=total_failed,
            success=success,
            topic=topic_name,
        )
    except Exception as e:
        return BatchPublishResult(
            results=results,
            total_sent=total_sent,
            total_failed=total_failed + len(events) - total_sent,
            success=False,
            error=str(e),
            topic=topic_name,
        )


if __name__ == "__main__":
    events = [
        {
            "event_id": "evt-batch-1",
            "event_type": "order.created",
            "source": "order-api",
            "payload": {"order_id": "ORD-001", "amount": 99.99},
        },
        {
            "event_id": "evt-batch-2",
            "event_type": "order.created",
            "source": "order-api",
            "payload": {"order_id": "ORD-002", "amount": 149.50},
        },
        {
            "event_id": "evt-batch-3",
            "event_type": "payment.processed",
            "source": "payment-service",
            "payload": {"payment_id": "PAY-001", "status": "completed"},
        },
    ]
    result = batch_publish(topic_name="events-topic", events=events)
    print(result.to_dict())
