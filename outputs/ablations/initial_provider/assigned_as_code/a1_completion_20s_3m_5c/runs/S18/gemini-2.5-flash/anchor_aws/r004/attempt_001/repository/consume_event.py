import json
import os

from messaging_client import get_sqs_client
from messaging_models import MessagePayload

def consume_event(queue_url=None, region_name=None):
    sqs_client = get_sqs_client(region_name)
    queue_url = queue_url or os.environ.get("SQS_QUEUE_URL")
    if not queue_url:
        raise ValueError("SQS Queue URL must be provided or set in environment variables.")

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])
    if messages:
        message = messages[0]
        receipt_handle = message["ReceiptHandle"]
        # Assuming the actual event is in the 'Message' attribute of the SQS message body
        # And the 'Message' attribute itself is a JSON string from SNS
        sns_message_body = json.loads(message["Body"])
        event_payload = json.loads(sns_message_body["Message"])
        payload = MessagePayload(event_payload)
        
        return {
            "payload": payload,
            "receipt_handle": receipt_handle,
            "message_id": message["MessageId"]
        }
    return None

def delete_consumed_event(receipt_handle, queue_url=None, region_name=None):
    sqs_client = get_sqs_client(region_name)
    queue_url = queue_url or os.environ.get("SQS_QUEUE_URL")
    if not queue_url:
        raise ValueError("SQS Queue URL must be provided or set in environment variables.")
    
    sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return {"status": "Message deleted"}
