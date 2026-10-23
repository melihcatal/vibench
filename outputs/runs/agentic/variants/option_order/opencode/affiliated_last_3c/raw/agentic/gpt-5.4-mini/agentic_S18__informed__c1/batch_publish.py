import json
import os
import boto3


def batch_publish(messages):
    sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))
    topic_arn = os.environ["SNS_TOPIC_ARN"]
    results = []
    for item in messages:
        body = json.dumps(item.get("payload", item))
        resp = sns.publish(
            TopicArn=topic_arn,
            Message=body,
            MessageAttributes={
                "message-id": {
                    "DataType": "String",
                    "StringValue": str(item.get("id", "")),
                }
            },
        )
        results.append(resp.get("MessageId"))
    return {"provider": "amazon-sns", "topic": topic_arn, "message_ids": results}
