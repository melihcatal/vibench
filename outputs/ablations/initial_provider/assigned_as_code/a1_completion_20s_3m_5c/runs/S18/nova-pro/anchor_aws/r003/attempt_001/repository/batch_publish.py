import boto3

from messaging_client import get_client


def batch_publish(payloads, config=None):
    config = config or {}
    client = get_client("sns", config)
    messages = [{"Message": json.dumps(payload)} for payload in payloads]
    response = client.publish_batch(TopicArn=config["topic_arn"], PublishBatchRequestEntries=messages)
    return {"message_ids": [entry["MessageId"] for entry in response["Successful"]]}