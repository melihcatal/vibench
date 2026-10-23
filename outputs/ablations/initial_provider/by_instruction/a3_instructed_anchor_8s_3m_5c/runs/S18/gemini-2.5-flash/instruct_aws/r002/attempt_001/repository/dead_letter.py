import boto3
import json
from messaging_client import get_sqs_dead_letter_queue_url

def send_to_dead_letter_queue(message_body: dict, original_message_id: str, error_details: str):
    """
    Sends a failed message to an AWS SQS Dead-Letter Queue.
    """
    sqs_client = boto3.client('sqs')
    dlq_url = get_sqs_dead_letter_queue_url()

    try:
        message_attributes = {
            'OriginalMessageId': {
                'DataType': 'String',
                'StringValue': original_message_id
            },
            'ErrorDetails': {
                'DataType': 'String',
                'StringValue': error_details
            }
        }

        response = sqs_client.send_message(
            QueueUrl=dlq_url,
            MessageBody=json.dumps(message_body),
            MessageAttributes=message_attributes
        )
        print(f"Message sent to DLQ: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"Error sending message to DLQ: {e}")
        raise

if __name__ == "__main__":
    failed_payload = {"data": "corrupted_data", "attempt": 3}
    original_id = "some-original-message-id-123"
    error_info = "Processing failed due to schema mismatch."
    send_to_dead_letter_queue(failed_payload, original_id, error_info)
