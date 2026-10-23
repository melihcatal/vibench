import os
import json
from messaging_client import get_sqs_client
from messaging_models import EventMessage, ConsumeResponse

def consume_event(queue_url: str) -> ConsumeResponse or None:
    sqs_client = get_sqs_client()
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get('Messages', [])
    if not messages:
        return None

    message = messages[0]
    message_body = json.loads(message['Body'])

    # For SNS-SQS integration, the actual message payload is in the 'Message' attribute of the SQS message body
    if 'Message' in message_body and 'TopicArn' in message_body:
        parsed_message = json.loads(message_body['Message'])
        event_type = message_body.get('MessageAttributes', {}).get('EventType', {}).get('Value', 'unknown')
        event_id = parsed_message.get('id', message['MessageId'])
        payload = parsed_message.get('payload', parsed_message) # Allow direct payload or wrapped one
    else:
        event_type = 'generic'
        event_id = message_body.get('id', message['MessageId'])
        payload = message_body.get('payload', message_body)

    event = EventMessage(
        id=event_id,
        event_type=event_type,
        payload=payload
    )

    # In a real scenario, you'd process the message before deleting it.
    # For this task, we delete it immediately after consumption.
    sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )

    return ConsumeResponse(
        event=event,
        raw_message_id=message['MessageId']
    )
