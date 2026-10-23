import boto3

from messaging_client import get_client


def dead_letter(payload, config=None):
    config = config or {}
    client = get_client("sns", config)
    response = client.publish(TopicArn=config["dead_letter_topic_arn"], Message=json.dumps(payload))
    return {"message_id": response["MessageId"]}