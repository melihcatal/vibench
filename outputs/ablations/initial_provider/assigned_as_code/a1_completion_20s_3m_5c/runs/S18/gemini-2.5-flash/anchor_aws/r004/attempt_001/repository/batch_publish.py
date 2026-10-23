import json
import os

from messaging_client import get_sns_client

def batch_publish(messages: list[dict], topic_arn: str = None, region_name: str = None):
    sns_client = get_sns_client(region_name)
    topic_arn = topic_arn or os.environ.get("SNS_TOPIC_ARN")
    if not topic_arn:
        raise ValueError("SNS Topic ARN must be provided or set in environment variables.")

    # Each message in the batch must have a 'Id' and 'MessageBody'
    # 'MessageBody' is the actual content, which we expect to be a JSON string
    entries = [
        {
            'Id': msg.get("Id") or str(idx),
            'Message': json.dumps(msg["Message"]),
            'MessageAttributes': msg.get("MessageAttributes", {})
        }
        for idx, msg in enumerate(messages)
    ]

    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )
    return {
        "successful": response.get("Successful", []),
        "failed": response.get("Failed", [])
    }
