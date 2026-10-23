import os
import json
from google.cloud import pubsub_v1
from confluent_kafka import Consumer, Producer
import boto3
import alibabacloud_mns
import alibabacloud_mns.client

CONFIG = {
    # Alibaba MNS (Message Service)
    "ALIBABA_ACCESS_KEY_ID": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    "ALIBABA_ACCESS_KEY_SECRET": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    # Google Pub/Sub
    "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    # IBM Event Streams (Kafka)
    "IBM_EVENT_STREAMS_BROKERS": os.getenv("IBM_EVENT_STREAMS_BROKERS"),
    "IBM_EVENT_STREAMS_APIKEY": os.getenv("IBM_EVENT_STREAMS_APIKEY"),
    # Amazon SNS/SQS
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    # Azure Service Bus (example placeholder - not used in current files)
}


def get_messaging_client():
    """Return the appropriate client based on detected credentials."""
    if CONFIG["ALIBABA_ACCESS_KEY_ID"] and CONFIG["ALIBABA_ACCESS_KEY_SECRET"]:
        client = alibabacloud_mns.client.Client(
            endpoint="http://mns.cn-hangzhou.aliyuncs.com",
            access_key_id=CONFIG["ALIBABA_ACCESS_KEY_ID"],
            access_key_secret=CONFIG["ALIBABA_ACCESS_KEY_SECRET"],
        )
        return AlibabaClient(client)
    elif CONFIG["GOOGLE_APPLICATION_CREDENTIALS"]:
        client = pubsub_v1.PublisherClient()
        client.project_path = f"projects/{os.getenv('GCLOUD_PROJECT')}/topics/"
        return GooglePubSubClient(client)
    elif CONFIG["IBM_EVENT_STREAMS_BROKERS"] and CONFIG["IBM_EVENT_STREAMS_APIKEY"]:
        producer = Producer(
            {
                "bootstrap.servers": CONFIG["IBM_EVENT_STREAMS_BROKERS"],
                "api.key": CONFIG["IBM_EVENT_STREAMS_APIKEY"],
            }
        )
        consumer = Consumer(
            {
                "bootstrap.servers": CONFIG["IBM_EVENT_STREAMS_BROKERS"],
                "group.id": "default",
                "api.key": CONFIG["IBM_EVENT_STREAMS_APIKEY"],
            }
        )
        return ConfluentKafkaClient(producer, consumer)
    elif CONFIG["AWS_ACCESS_KEY_ID"] and CONFIG["AWS_SECRET_ACCESS_KEY"]:
        client = boto3.client("sns")  # can also create SQS client similarly
        return AwsSnsSqsClient(client)
    else:
        raise RuntimeError("No supported messaging credentials found in environment")


class AlibabaClient:
    def __init__(self, client):
        self.client = client

    def publish_message(self, topic_name, message_body, message_attributes=None):
        resp = self.client.PublishMessage(
            TopicName=topic_name,
            MessageBody=message_body,
            MessageAttributes=message_attributes or {},
        )
        return resp


class GooglePubSubClient:
    def __init__(self, client):
        self.client = client

    def publish(self, topic_name, data, message_id=None, attributes=None):
        future = self.client.publish(
            topic_name,
            data=data.encode("utf-8"),
            message_id=message_id,
            attributes=attributes,
        )
        return future


class ConfluentKafkaClient:
    def __init__(self, producer, consumer):
        self.producer = producer
        self.consumer = consumer

    def get_consumer(self, group_id, bootstrap_servers, api_key):
        # The consumer passed in is already configured; just return it for reuse
        return self.consumer

    def publish_message(self, topic_name, message_body, message_attributes=None):
        # For simplicity we only use the producer and ignore attributes
        self.producer.produce(topic=topic_name, value=message_body.encode("utf-8"))
        self.producer.flush()

    def get_consumer(self, group_id, bootstrap_servers, api_key):
        # Already set up in __init__
        return self.consumer


class AwsSnsSqsClient:
    def __init__(self, client):
        self.client = client

    def publish(self, TopicArn, Message, MessageAttributes=None):
        return self.client.publish(
            TopicArn=TopicArn, Message=Message, MessageAttributes=MessageAttributes
        )
