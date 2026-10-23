import boto3
import os
import json
from typing import List, Dict


def batch_publish_events(
    topic_arn: str, messages: List[Dict], region_name: str = "us-east-1"
):
    """
    Publishes a batch of JSON events to an AWS SNS topic.
    Messages should be a list of dictionaries, each with 'Id' and 'Message' keys.
    """
    sns_client = boto3.client(
        "sns",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )
    entries = []
    for i, msg in enumerate(messages):
        entries.append(
            {
                "Id": msg.get("Id", str(i)),
                "Message": json.dumps(msg.get("Message", {})),
                "MessageStructure": "json",
            }
        )

    response = sns_client.publish_batch(
        TopicArn=topic_arn, PublishBatchRequestEntries=entries
    )
    return response
