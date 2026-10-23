import boto3


def batch_publish(payload, config=None):
    config = config or {}
    client = boto3.client("sns", region_name=config.get("region"))
    results = []
    for item in payload["messages"]:
        response = client.publish(
            TopicArn=config["topic_arn"],
            Message=item["body"],
            MessageAttributes=item.get("attributes", {}),
        )
        results.append({"id": item.get("id"), "message_id": response["MessageId"]})
    return {"messages": results}
