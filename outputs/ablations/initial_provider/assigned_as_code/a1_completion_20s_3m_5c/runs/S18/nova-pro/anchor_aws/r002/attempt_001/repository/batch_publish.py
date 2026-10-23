import boto3

from messaging_models import normalize_payload


def batch_publish(payloads, config=None):
    config = config or {}
    client = boto3.client("sns", region_name=config.get("region"))
    normalized_payloads = [normalize_payload(payload) for payload in payloads]
    response = client.publish_batch(
        TopicArn=config["topic_arn"],
        PublishBatchRequestEntries=[{"Id": str(i), "Message": json.dumps(payload)} for i, payload in enumerate(normalized_payloads)]
    )
    return [{"message_id": entry["MessageId"]} for entry in response["Successful"]]