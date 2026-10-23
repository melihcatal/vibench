import boto3

from messaging_models import normalize_payload


def dead_letter(payload, config=None):
    config = config or {}
    client = boto3.client("sns", region_name=config.get("region"))
    normalized_payload = normalize_payload(payload)
    response = client.publish(TopicArn=config["dead_letter_topic_arn"], Message=json.dumps(normalized_payload))
    return {"message_id": response["MessageId"]}