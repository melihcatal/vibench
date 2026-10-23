import boto3

from messaging_client import get_client


def consume_event(config=None):
    config = config or {}
    client = get_client("sqs", config)
    response = client.receive_message(QueueUrl=config["queue_url"], MaxNumberOfMessages=1, WaitTimeSeconds=10)
    messages = response.get("Messages", [])
    if messages:
        return json.loads(messages[0]["Body"])
    return None