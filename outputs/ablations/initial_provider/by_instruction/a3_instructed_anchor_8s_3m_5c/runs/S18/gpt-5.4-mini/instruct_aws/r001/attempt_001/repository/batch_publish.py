import json
import os

from messaging_client import sns_client, sns_topic_arn, sqs_client, sqs_queue_url
from messaging_models import parse_json_payload, normalize_payload


def batch_publish(messages):
    topic_arn = sns_topic_arn()
    if topic_arn:
        client = sns_client()
        results = []
        for item in messages:
            response = client.publish(TopicArn=topic_arn, Message=normalize_payload(item))
            results.append({"id": item.get("id"), "message_id": response["MessageId"]})
        return {"successful": results, "failed": []}
    client = sqs_client()
    results = []
    for item in messages:
        response = client.send_message(QueueUrl=sqs_queue_url(), MessageBody=normalize_payload(item))
        results.append({"id": item.get("id"), "message_id": response["MessageId"]})
    return {"successful": results, "failed": []}


if __name__ == "__main__":
    messages = parse_json_payload(os.getenv("BATCH_MESSAGES", "[]"))
    print(json.dumps(batch_publish(messages)))
