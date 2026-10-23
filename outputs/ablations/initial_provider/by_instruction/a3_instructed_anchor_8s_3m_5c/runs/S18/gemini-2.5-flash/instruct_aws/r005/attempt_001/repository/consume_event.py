import os
import json
from messaging_client import MessagingClient
from messaging_models import MessagePayload

def consume_event():
    sqs_client = MessagingClient().get_sqs_client() # Assuming get_sqs_client will be added to MessagingClient
    queue_url = os.environ.get('AWS_SQS_QUEUE_URL')

    if not queue_url:
        raise ValueError("AWS_SQS_QUEUE_URL environment variable not set.")

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    messages = response.get('Messages', [])
    if messages:
        message = messages[0]
        # Assuming the message body is a JSON string containing the SNS message
        # and the actual payload is nested within a 'Message' key if from SNS
        try:
            body = json.loads(message['Body'])
            if 'Message' in body:
                message_content = json.loads(body['Message'])
                # Reconstruct MessagePayload from the inner content
                payload = MessagePayload(
                    message_content.get('message_id'),
                    message_content.get('content'),
                    message_content.get('source')
                )
            else:
                # If it's a direct SQS message, assume the body is the payload
                payload = MessagePayload(
                    body.get('message_id'),
                    body.get('content'),
                    body.get('source')
                )
        except json.JSONDecodeError:
            # Handle cases where the body is not JSON or not in expected format
            payload = MessagePayload(
                "unknown",
                message['Body'],
                "unknown"
            )

        # Delete the message from the queue
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
        return payload, message['ReceiptHandle']
    return None, None
