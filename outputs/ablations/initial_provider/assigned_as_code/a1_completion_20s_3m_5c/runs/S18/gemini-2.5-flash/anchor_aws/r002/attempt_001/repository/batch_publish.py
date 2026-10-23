import json
from messaging_client import get_sns_client
from messaging_models import MessagePayload

def batch_publish(topic_arn, payloads, config=None):
    config = config or {}
    sns_client = get_sns_client(config.get("region"))
    entries = []
    for i, payload in enumerate(payloads):
        entries.append({
            "Id": str(i),
            "Message": MessagePayload(payload["event_id"], payload["event_type"], payload["data"]).to_json()
        })

    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )
    return {"successful": response.get("Successful", []), "failed": response.get("Failed", [])}
