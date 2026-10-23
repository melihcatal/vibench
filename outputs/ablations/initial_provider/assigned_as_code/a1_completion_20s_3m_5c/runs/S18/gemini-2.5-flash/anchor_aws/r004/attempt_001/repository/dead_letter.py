import json
import os

from messaging_client import get_sqs_client

def send_to_dead_letter_queue(original_message_body: dict, dead_letter_queue_url: str, region_name: str = None):
    sqs_client = get_sqs_client(region_name)
    
    # The message body should contain enough information to understand what failed
    # For this example, we'll stringify the original message body
    message_body_str = json.dumps(original_message_body)

    response = sqs_client.send_message(
        QueueUrl=dead_letter_queue_url,
        MessageBody=message_body_str,
        MessageAttributes={
            'FailureReason': {
                'StringValue': 'Message processing failed',
                'DataType': 'String'
            }
        }
    )
    return {"status": "Sent to dead-letter queue", "message_id": response["MessageId"]}
