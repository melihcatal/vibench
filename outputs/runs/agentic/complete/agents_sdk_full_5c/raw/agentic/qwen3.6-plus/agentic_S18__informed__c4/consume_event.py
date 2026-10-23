"""
Consume one message from a Google Cloud Pub/Sub managed subscription.

Uses the google-cloud-pubsub SDK to connect to the Pub/Sub subscriber
authenticated via GOOGLE_APPLICATION_CREDENTIALS.
"""

import sys
from concurrent.futures import TimeoutError as FuturesTimeoutError
from messaging_client import (
    get_subscriber_client,
    subscription_path,
    ensure_subscription_exists,
)
from messaging_models import PubSubEvent, ConsumeResult


def consume_event(
    subscription_name: str | None = None,
    topic_name: str | None = None,
    timeout_seconds: float = 30.0,
) -> ConsumeResult:
    """
    Consume a single message from a Google Cloud Pub/Sub subscription.

    Receives exactly one message, acknowledges it, and returns a normalized
    ConsumeResult.

    Args:
        subscription_name: Override the default subscription name.
        topic_name: The topic this subscription is attached to (for auto-creation).
        timeout_seconds: How long to wait for a message before timing out.

    Returns:
        ConsumeResult containing the received event or an error.
    """
    subscriber = get_subscriber_client()
    sub_path = ensure_subscription_exists(
        subscription_name=subscription_name,
        topic_name=topic_name,
    )

    result_holder: list[ConsumeResult] = []

    def callback(message):
        try:
            event = PubSubEvent.from_subscriber_message(message)
            message.ack()
            result_holder.append(
                ConsumeResult(event=event, acknowledged=True)
            )
        except Exception as exc:
            message.nack()
            result_holder.append(
                ConsumeResult(event=None, acknowledged=False, nack=True, error=str(exc))
            )

    streaming_pull_future = subscriber.subscribe(sub_path, callback=callback)

    try:
        streaming_pull_future.result(timeout=timeout_seconds)
    except FuturesTimeoutError:
        if not result_holder:
            result_holder.append(
                ConsumeResult(event=None, acknowledged=False, error="Timeout waiting for message")
            )
    except Exception as exc:
        result_holder.append(
            ConsumeResult(event=None, acknowledged=False, error=str(exc))
        )
    finally:
        streaming_pull_future.cancel()
        streaming_pull_future.result(timeout=5)

    return result_holder[0] if result_holder else ConsumeResult(
        event=None, acknowledged=False, error="No result produced"
    )


if __name__ == "__main__":
    import json
    result = consume_event(timeout_seconds=30.0)
    print(json.dumps(result.to_dict(), indent=2, default=str))
