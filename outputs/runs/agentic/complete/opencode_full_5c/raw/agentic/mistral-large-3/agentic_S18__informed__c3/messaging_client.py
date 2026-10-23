from google.cloud import pubsub_v1
import json
import os


class PubSubClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id):
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id):
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    def publish_message(self, topic_id, data, attributes=None):
        topic_path = self.get_topic_path(topic_id)
        data_bytes = json.dumps(data).encode("utf-8")
        future = self.publisher.publish(topic_path, data_bytes, **(attributes or {}))
        return future.result()

    def pull_message(self, subscription_id, timeout=None):
        subscription_path = self.get_subscription_path(subscription_id)
        response = self.subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": 1,
                "return_immediately": False,
            },
            timeout=timeout,
        )
        if response.received_messages:
            message = response.received_messages[0]
            self.subscriber.acknowledge(
                request={
                    "subscription": subscription_path,
                    "ack_ids": [message.ack_id],
                }
            )
            return {
                "id": message.message.message_id,
                "data": json.loads(message.message.data.decode("utf-8")),
                "attributes": message.message.attributes,
            }
        return None

    def publish_batch(self, topic_id, messages):
        topic_path = self.get_topic_path(topic_id)
        futures = []
        for message in messages:
            data_bytes = json.dumps(message["data"]).encode("utf-8")
            future = self.publisher.publish(
                topic_path, data_bytes, **(message.get("attributes", {}) or {})
            )
            futures.append(future)
        return [future.result() for future in futures]

    def dead_letter_message(self, topic_id, data, attributes=None):
        attributes = attributes or {}
        attributes["dead_letter_reason"] = attributes.get(
            "dead_letter_reason", "unknown"
        )
        return self.publish_message(topic_id, data, attributes)
