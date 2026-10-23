import json

import boto3


def batch_publish(payload, config=None):
    config = config or {}
    client = boto3.client("sns", region_name=config.get("region"))
    results = []
    for item in payload["events"]:
        response = client.publish(TopicArn=config["topic_arn"], Message=json.dumps(item["event"]), MessageAttributes=item.get("attributes", {}))
        results.append({"id": item.get("id"), "message_id": response["MessageId"]})
    return {"results": results}
