import boto3
import json

def send_to_dead_letter_queue(dead_letter_queue_url: str, message_body: dict, message_attributes: dict = None):
    sqs_client = boto3.client('sqs')  # AWS SDK import
    if message_attributes is None:
        message_attributes = {}

    # Convert message_attributes to the format expected by SQS
    sqs_message_attributes = {
        k: {'DataType': 'String', 'StringValue': str(v)} for k, v in message_attributes.items()
    }

    response = sqs_client.send_message(
        QueueUrl=dead_letter_queue_url,
        MessageBody=json.dumps(message_body),
        MessageAttributes=sqs_message_attributes
    )
    return response
