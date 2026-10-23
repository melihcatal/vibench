import json
import os
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber import message as sub_message
from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import ConsumedEvent, ConsumeResponse


def consume_event(
    acknowledge: bool = True, max_wait_seconds: int = 5
) -> ConsumeResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription")

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    received_messages = []

    def callback(message: sub_message.Message):
        try:
            payload = json.loads(message.data.decode("utf-8"))
            event = ConsumedEvent(
                message_id=message.message_id,
                data=payload,
                attributes=dict(message.attributes),
                publish_time=message.publish_time.isoformat()
                if message.publish_time
                else None,
            )
            received_messages.append(event)
            if acknowledge:
                message.ack()
        except (json.JSONDecodeError, UnicodeDecodeError):
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result(timeout=max_wait_seconds)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

    if received_messages:
        event = received_messages[0]
        return ConsumeResponse(
            event=event, status="consumed", subscription_path=subscription_path
        )

    return ConsumeResponse(
        event=None, status="no_messages", subscription_path=subscription_path
    )


if __name__ == "__main__":
    response = consume_event(acknowledge=True)
    print(json.dumps(response.to_dict(), indent=2, default=str))
