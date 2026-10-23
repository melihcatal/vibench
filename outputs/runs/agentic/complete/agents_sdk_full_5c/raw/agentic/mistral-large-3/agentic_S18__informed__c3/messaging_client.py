# Local configuration and client helper utilities for Google Cloud Pub/Sub
from google.cloud import pubsub_v1
from google.api_core import retry
from google.api_core.exceptions import GoogleAPICallError
from typing import Optional, Dict, Any, List
import os
from messaging_models import PubSubMessage, BatchPublishRequest, DeadLetterRequest


class PubSubClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.retry = retry.Retry(deadline=30.0)

    def get_topic_path(self, topic: str) -> str:
        return self.publisher.topic_path(self.project_id, topic)

    def get_subscription_path(self, subscription: str) -> str:
        return self.subscriber.subscription_path(self.project_id, subscription)

    def publish_message(self, topic: str, message: PubSubMessage) -> str:
        topic_path = self.get_topic_path(topic)
        future = self.publisher.publish(
            topic_path,
            data=message.to_json().encode("utf-8"),
            **{
                "message_id": message.attributes.message_id,
                **message.attributes.attributes
            }
        )
        return future.result()

    def publish_batch(self, request: BatchPublishRequest) -> List[str]: 
        topic_path = self.get_topic_path(request.topic)
        futures = []
        for message in request.messages:
            future = self.publisher.publish(
                topic_path,
                data=message.to_json().encode("utf-8"),
                **{
                    "message_id": message.attributes.message_id,
                    **message.attributes.attributes
                }
            )
            futures.append(future)
        return [future.result() for future in futures]

    def pull_message(self, subscription: str, timeout: Optional[float] = None) -> Optional[PubSubMessage]:
        subscription_path = self.get_subscription_path(subscription)
        response = self.subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": 1,
                "return_immediately": False
            },
            retry=self.retry,
            timeout=timeout
        )
        if not response.received_messages:
            return None
        received_message = response.received_messages[0]
        message = PubSubMessage.from_json(received_message.message.data.decode("utf-8"))
        self.subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [received_message.ack_id]
            }
        )
        return message

    def dead_letter_message(self, request: DeadLetterRequest) -> str:
        topic_path = self.get_topic_path(request.dead_letter_topic)
        future = self.publisher.publish(
            topic_path,
            data=request.failed_message.to_json().encode("utf-8"),
            error_details=json.dumps(request.error_details).encode("utf-8"),
            **{
                "message_id": request.failed_message.attributes.message_id,
                **request.failed_message.attributes.attributes
            }
        )
        return future.result()