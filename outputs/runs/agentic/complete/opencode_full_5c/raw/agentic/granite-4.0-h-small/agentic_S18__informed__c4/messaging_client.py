import os
import json

# Choose the active provider via environment variables
PROVIDER = os.getenv("PUBSUB_PROVIDER", "aws")

if PROVIDER == "aws":
    import boto3
    from botocore.exceptions import ClientError

    def get_pubsub_client():
        """Return an AWS SNS client (publish) and SQS client (consume)."""
        sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))
        sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-east-1"))
        return type(
            "Clients",
            (),
            {
                "publish": sns.publish,
                "receive": lambda sub: sqs.receive_message(
                    QueueUrl=os.getenv("AWS_SQS_URL")
                ),
                "acknowledge": lambda _: None,
                "publish_batch": lambda _: None,
            },
        )

    def get_sub_client():
        import boto3

        sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-east-1"))
        return type(
            "Client",
            (),
            {
                "receive": lambda _: sqs.receive_message(
                    QueueUrl=os.getenv("AWS_SQS_URL")
                ),
                "acknowledge": lambda _: None,
            },
        )
elif PROVIDER == "gcp":
    from google.cloud import pubsub_v1
    from google.cloud import storage

    def get_pubsub_client():
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        return type(
            "Clients",
            (),
            {
                "publish": lambda t, m: publisher.publish(
                    t, data=json.dumps(m).encode()
                ),
                "receive": lambda sub: (
                    subscriber.pull(sub, max_messages=1)[0]
                    if subscriber.pull(sub, max_messages=1)
                    else None
                ),
                "acknowledge": lambda m: subscriber.acknowledge(
                    subscriber.subscription_path("project", sub), [m.ack_id]
                ),
                "publish_batch": lambda _: None,
            },
        )
elif PROVIDER == "azure":
    from azure.servicebus import ServiceBusClient, ServiceBusMessage

    def get_pubsub_client():
        service_bus_client = ServiceBusClient.from_connection_string(
            os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
        )
        return type(
            "Clients",
            (),
            {
                "publish": lambda t, m: service_bus_client.send_message(
                    t, ServiceBusMessage(m)
                ),
                "receive": lambda sub: service_bus_client.receive_messages(
                    sub, max_message_count=1
                ),
                "acknowledge": lambda m: None,
                "publish_batch": lambda t, msgs: service_bus_client.send_messages(
                    t, [ServiceBusMessage(m) for m in msgs]
                ),
            },
        )
else:
    raise RuntimeError("Unsupported PUBSUB_PROVIDER")

# Simple event serialization (convert to JSON string)
serialize_event = lambda ev: json.dumps(ev)
