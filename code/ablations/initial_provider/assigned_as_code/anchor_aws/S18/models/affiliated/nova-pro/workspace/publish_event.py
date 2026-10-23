import json

import boto3


def publish_event(payload, config=None):
    config = config or {}
    client = boto3.client("sns", region_name=config.get("region"))
    response = client.publish(TopicArn=config["topic_arn"], Message=json.dumps(payload["event"]))
    return {"message_id": response["MessageId"]}
