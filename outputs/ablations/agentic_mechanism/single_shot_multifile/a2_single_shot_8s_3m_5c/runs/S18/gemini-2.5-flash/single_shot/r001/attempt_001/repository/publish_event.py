import json
import os
from messaging_client import get_sns_client

def publish_event(message_payload: dict, topic_arn: str):
    sns_client = get_sns_client()
    message_json = json.dumps(message_payload)
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message_json,
        MessageStructure='string'
    )
    return response