import json
import os
from typing import List, Dict, Any

import boto3

from messaging_client import get_sns_client, create_sns_message_attributes
from messaging_models import PublishRequest, PublishResponse

def batch_publish_event(topic_arn: str, region_name: str, publish_requests: List[PublishRequest]):
    sns_client = get_sns_client(region_name)

    entries = []
    for i, req in enumerate(publish_requests):
        entry = {
            'Id': str(i),  # Unique identifier for each message in the batch
            'Message': json.dumps(req.event_data),
        }
        if req.message_attributes:
            entry['MessageAttributes'] = create_sns_message_attributes(req.message_attributes)
        entries.append(entry)

    if not entries:
        return {"Failed": [], "Successful": []}

    # SNS PublishBatch supports up to 10 messages per call
    # We might need to split if publish_requests is larger than 10
    batch_size = 10
    successful_messages = []
    failed_messages = []

    for i in range(0, len(entries), batch_size):
        batch = entries[i:i + batch_size]
        response = sns_client.publish_batch(
            TopicArn=topic_arn,
            PublishBatchRequestEntries=batch
        )
        successful_messages.extend([PublishResponse(message_id=msg["MessageId"]) for msg in response.get("Successful", [])])
        failed_messages.extend(response.get("Failed", []))

    return {"Successful": [msg.message_id for msg in successful_messages], "Failed": failed_messages}
