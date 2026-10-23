import os
import json
from messaging_client import MessagingClient
from messaging_models import MessagePayload

def send_to_dead_letter(message_payload: MessagePayload, original_receipt_handle: str = None):
    sqs_client = MessagingClient().get_sqs_client()
    dlq_url = os.environ.get('AWS_SQS_DEAD_LETTER_QUEUE_URL')

    if not dlq_url:
        raise ValueError("AWS_SQS_DEAD_LETTER_QUEUE_URL environment variable not set.")

    message_body = message_payload.to_json()
    
    # Optionally include the original receipt handle or other metadata for debugging
    message_attributes = {
        'SourceReceiptHandle': {
            'DataType': 'String',
            'StringValue': original_receipt_handle if original_receipt_handle else 'N/A'
        },
        'MessageType': {
            'DataType': 'String',
            'StringValue': 'DeadLetterMessage'
        }
    }

    response = sqs_client.send_message(
        QueueUrl=dlq_url,
        MessageBody=message_body,
        MessageAttributes=message_attributes
    )
    return response
