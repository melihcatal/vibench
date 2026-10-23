import json

from messaging_client import get_sqs_client
from messaging_models import ConsumeResponse, Message


def consume_event(config=None):
    config = config or {}
    sqs_client = get_sqs_client(config.get("region"))
    response = sqs_client.receive_message(
        QueueUrl=config["queue_url"],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    messages = []
    if "Messages" in response:
        for msg in response["Messages"]:
            body = json.loads(msg["Body"])
            # Assuming the actual message content is within an 'Message' key if from SNS
            message_content = json.loads(body.get('Message', '{}')) if 'Message' in body else body
            messages.append(Message(
                id=msg["MessageId"],
                body=message_content,
                attributes=msg.get("MessageAttributes", None)
            ))
            # Delete the message after processing
            sqs_client.delete_message(
                QueueUrl=config["queue_url"],
                ReceiptHandle=msg["ReceiptHandle"]
            )
    return ConsumeResponse(messages=messages)
