import os
import json
from messaging_client import get_sns_client
from messaging_models import EventMessage

def batch_publish_events(topic_arn: str, messages: list[EventMessage]) -> dict:
    sns_client = get_sns_client()
    
    # SNS publish_batch allows up to 10 messages
    entries = []
    for i, message in enumerate(messages):
        entry = {
            'Id': message.id, 
            'Message': json.dumps(message.to_dict()),
            'MessageAttributes': {
                'EventType': {
                    'DataType': 'String',
                    'StringValue': message.event_type
                }
            }
        }
        entries.append(entry)

    if not entries:
        return {"Failed": [], "Successful": []}

    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )
    return response
