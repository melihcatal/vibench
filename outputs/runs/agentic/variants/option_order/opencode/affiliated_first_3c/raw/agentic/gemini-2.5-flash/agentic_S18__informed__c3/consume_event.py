import json
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_project_id
from messaging_models import PubSubMessage


def consume_single_event(
    subscription_id: str, timeout: float = 5.0
) -> PubSubMessage | None:
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    messages = []

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        try:
            data_str = message.data.decode("utf-8")
            attributes = dict(message.attributes)
            messages.append(
                PubSubMessage(
                    id=message.message_id,
                    data=json.loads(data_str),
                    attributes=attributes,
                )
            )
            message.ack()
        except Exception as e:
            print(f"Error processing message: {e}")
            message.nack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except Exception as e:
        print(f"Listening for messages on {subscription_path} threw an exception: {e}")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

    return messages[0] if messages else None
