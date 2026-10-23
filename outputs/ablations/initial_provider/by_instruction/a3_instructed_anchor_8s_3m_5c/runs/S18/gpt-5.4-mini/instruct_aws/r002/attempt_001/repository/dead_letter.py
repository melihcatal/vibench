import json
from messaging_client import resolve_queue_url, sqs_client
from messaging_models import normalize_message_body


def dead_letter(payload, queue_url=None):
    body = normalize_message_body(payload)
    response = sqs_client().send_message(
        QueueUrl=resolve_queue_url(queue_url),
        MessageBody=body,
    )
    return {"message_id": response["MessageId"], "body": body}


def main():
    payload = json.loads(input())
    print(json.dumps(dead_letter(payload)))


if __name__ == "__main__":
    main()
