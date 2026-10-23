import os
from typing import List
from messaging_client import MessagingClient
from messaging_models import MessagePayload

def batch_publish_events(message_payloads: List[MessagePayload]):
    sns_client = MessagingClient().get_sns_client()
    topic_arn = os.environ.get('AWS_SNS_TOPIC_ARN')

    if not topic_arn:
        raise ValueError("AWS_SNS_TOPIC_ARN environment variable not set.")

    responses = []
    for payload in message_payloads:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=payload.to_json(),
            MessageAttributes={
                'message_id': {
                    'DataType': 'String',
                    'StringValue': payload.message_id
                },
                'source': {
                    'DataType': 'String',
                    'StringValue': payload.source
                }
            }
        )
        responses.append(response)
    return responses
