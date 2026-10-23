import json

import boto3


def message_summary(payload, config=None):
    config = config or {}
    client = boto3.client("sns", region_name=config.get("region"))
    data = payload.get("results", payload)
    return {"summary": json.dumps({"count": len(data) if hasattr(data, "__len__") else 1, "service": "aws-sns"}), "topic_arn": config.get("topic_arn")}
