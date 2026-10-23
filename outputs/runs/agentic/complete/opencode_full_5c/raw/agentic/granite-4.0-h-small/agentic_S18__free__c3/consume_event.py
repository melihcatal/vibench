import json

# [SAME-SCENARIO] consume_event.py
# Consumes one message from a managed subscription using AWS SQS (standard queue) named 'my-message-queue'

from messaging_client import get_sqs_client

def consume_event(queue_url: str) -> dict:
    """Consume a single message from an SQS queue and return the message data.
    
    Args:
        queue_url (str): URL of the SQS queue.
    """
    client = get_sqs_client()
    response = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    messages = response.get('Messages', [])
    if messages:
        message = messages[0]
        receipt_handle = message['ReceiptHandle']
        # return both the body and receipt handle for later delete
n        return {'body': json.loads(message['Body']), 'receipt_handle': receipt_handle}
    return None
