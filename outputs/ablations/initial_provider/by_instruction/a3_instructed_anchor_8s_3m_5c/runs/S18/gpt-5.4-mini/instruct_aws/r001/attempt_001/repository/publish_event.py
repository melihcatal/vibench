import json
import os

from messaging_client import sns_client, sns_topic_arn, sqs_client, sqs_queue_url
from messaging_models import normalize_payload


def publish_event(event):
    payload = normalize_payload(event)
    topic_arn = sns_topic_arn()
    if topic_arn:
        response = sns_client().publish(TopicArn=topic_arn, Message=payload)
        return {"message_id": response["MessageId"], "destination": topic_arn}
    queue_url = sqs_queue_url()
    response = sqs_client().send_message(QueueUrl=queue_url, MessageBody=payload)
    return {"message_id": response["MessageId"], "destination": queue_url}


def main():
    raw = os.getenv("EVENT_PAYLOAD", "{}")
    event = json.loads(raw)
    result = publish_event(event)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
