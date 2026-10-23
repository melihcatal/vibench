import json

import boto3

from messaging_client import get_sns_sqs_client_config, normalize_batch_items


def batch_publish(payload, config=None):
    config = get_sns_sqs_client_config(config)
    client = boto3.client("sns", region_name=config["region"])
    items = normalize_batch_items(payload)
    entries = []
    for index, item in enumerate(items[:10]):
        entries.append(
            {
                "Id": item.get("id") or str(index),
                "Message": json.dumps(item["event"]),
                "MessageAttributes": item.get("attributes", {}),
            }
        )
    response = client.publish_batch(TopicArn=config["topic_arn"], PublishBatchRequestEntries=entries)
    return {"successful": response.get("Successful", []), "failed": response.get("Failed", [])}
