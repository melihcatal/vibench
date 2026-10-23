import os
from messaging_client import MessagingClient
from messaging_models import MessagePayload

def publish_event(message_id: str, content: str, source: str):
    sns_client = MessagingClient().get_sns_client()
    topic_arn = os.environ.get('AWS_SNS_TOPIC_ARN')

    if not topic_arn:
        raise ValueError("AWS_SNS_TOPIC_ARN environment variable not set.")

    payload = MessagePayload(message_id, content, source)
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=payload.to_json(),
        MessageAttributes={
            'message_id': {
                'DataType': 'String',
                'StringValue': message_id
            },
            'source': {
                'DataType': 'String',
                'StringValue': source
            }
        }
    )
    return response
