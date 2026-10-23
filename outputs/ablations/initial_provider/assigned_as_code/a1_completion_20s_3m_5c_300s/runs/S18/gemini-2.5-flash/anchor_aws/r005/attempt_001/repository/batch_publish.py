import json

from messaging_client import get_sns_client
from messaging_models import BatchPublishRequest, PublishResponse


def batch_publish(batch_request: BatchPublishRequest, config=None):
    config = config or {}
    sns_client = get_sns_client(config.get("region"))
    results = []
    for message_payload in batch_request.messages:
        response = sns_client.publish(
            TopicArn=batch_request.topic_arn,
            Message=json.dumps(message_payload["event"]),
            MessageAttributes={
                "message_id": {
                    "DataType": "String",
                    "StringValue": message_payload.get("id", "")
                }
            }
        )
        results.append(PublishResponse(message_id=response["MessageId"]))
    return {"published_messages": [res.message_id for res in results]}
