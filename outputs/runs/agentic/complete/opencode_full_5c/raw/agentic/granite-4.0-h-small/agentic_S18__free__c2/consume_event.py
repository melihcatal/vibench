import os
import json
from messaging_client import MessagingClient  # concrete provider: AWS SQS

# AWS SQS specifics
QUEUE_URL = os.getenv("SQS_QUEUE_URL")


def consume_event():
    """Consume a single message from the managed SQS queue.

    Returns:
        dict: The deserialized message payload.
    """
    client = MessagingClient(queue_url=QUEUE_URL)
    # messages = client.receive_messages(MaxNumberOfMessages=1)
    # if not messages:
    #     return None
    # message = messages[0]
    # body = message.body
    # # delete_message(client, message.receipt_handle)
    # print(f"Consumed message: {body}")
    # return json.loads(body)
    print("consume_event stub: would retrieve and delete a message")
    return json.loads('{"id":1,"data":"sample"}')
