import os
import json
import boto3


def batch_publish(topic_arn: str, messages: list[dict]):
    sns_client = boto3.client(
        "sns",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    entries = []
    for i, message in enumerate(messages):
        entries.append(
            {
                "Id": str(i),
                "Message": json.dumps(message),
                "MessageAttributes": {
                    "event_type": {
                        "DataType": "String",
                        "StringValue": message.get("event_type", "unknown"),
                    }
                },
            }
        )
    response = sns_client.publish_batch(
        TopicArn=topic_arn, PublishBatchRequestEntries=entries
    )
    return response
