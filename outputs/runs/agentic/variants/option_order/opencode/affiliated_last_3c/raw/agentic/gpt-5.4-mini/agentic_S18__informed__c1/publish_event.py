import json
import os
import boto3

from messaging_models import normalize_payload


def publish_event(event: dict) -> dict:
    sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))
    topic_arn = os.environ["SNS_TOPIC_ARN"]
    payload = normalize_payload(event)
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(payload),
        MessageAttributes={
            "content-type": {"DataType": "String", "StringValue": "application/json"}
        },
    )
    return {
        "provider": "amazon-sns",
        "topic": topic_arn,
        "message_id": response.get("MessageId"),
    }
