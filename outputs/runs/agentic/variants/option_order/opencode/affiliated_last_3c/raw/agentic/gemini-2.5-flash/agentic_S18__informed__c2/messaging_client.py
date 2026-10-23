import os
from google.cloud import pubsub_v1
from typing import List, Dict, Any, Optional
from messaging_models import PubSubMessage


class PubSubClient:
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish_message(self, topic_name: str, message: PubSubMessage) -> str:
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        future = self.publisher.publish(
            topic_path, message.to_json().encode("utf-8"), **message.attributes
        )
        return future.result()

    def publish_batch(
        self, topic_name: str, messages: List[PubSubMessage]
    ) -> List[str]:
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        futures = []
        for message in messages:
            future = self.publisher.publish(
                topic_path, message.to_json().encode("utf-8"), **message.attributes
            )
            futures.append(future)
        return [future.result() for future in futures]

    def consume_message(
        self, subscription_name: str, timeout: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        subscription_path = self.subscriber.subscription_path(
            self.project_id, subscription_name
        )

        def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            print(f"Received message: {message.data.decode('utf-8')}")
            message.ack()
            # Store the message for return value (this is a simplified example)
            # In a real application, you might use a queue or shared object
            self._last_consumed_message = {
                "data": message.data.decode("utf-8"),
                "attributes": dict(message.attributes),
                "message_id": message.message_id,
                "ack_id": message.ack_id,
            }

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path, callback=callback
        )
        self._last_consumed_message = None  # Reset before pulling

        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()  # Raise TimeoutError if appropriate
        except Exception as e:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            raise e

        return self._last_consumed_message

    def acknowledge_message(self, subscription_name: str, ack_ids: List[str]) -> None:
        subscription_path = self.subscriber.subscription_path(
            self.project_id, subscription_name
        )
        self.subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

    def send_to_dead_letter_topic(self, topic_name: str, message: PubSubMessage) -> str:
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        future = self.publisher.publish(
            topic_path, message.to_json().encode("utf-8"), **message.attributes
        )
        return future.result()
