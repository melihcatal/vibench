import os
import json
from messaging_client import get_sns_client
from messaging_models import EventMessage

def publish_event(topic_arn: str, message: EventMessage) -> dict:
    sns_client = get_sns_client()
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message.to_dict()),
        MessageAttributes={
            'EventType': {
                'DataType': 'String',
                'StringValue': message.event_type
            }
        }
    )
    return response
