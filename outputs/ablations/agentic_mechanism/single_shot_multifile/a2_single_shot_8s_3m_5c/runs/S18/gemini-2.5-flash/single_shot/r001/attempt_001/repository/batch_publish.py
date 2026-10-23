import json
import os
from typing import List, Dict
from messaging_client import get_sns_client

def publish_batch_events(messages: List[Dict], topic_arn: str):
    sns_client = get_sns_client()

    entries = []
    for msg in messages:
        if 'Id' not in msg or 'Message' not in msg:
            raise ValueError("Each message in batch must have 'Id' and 'Message' keys.")
        entries.append({
            'Id': str(msg['Id']),
            'Message': json.dumps(msg['Message']),
            'MessageStructure': 'string'
        })
    
    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )
    return response