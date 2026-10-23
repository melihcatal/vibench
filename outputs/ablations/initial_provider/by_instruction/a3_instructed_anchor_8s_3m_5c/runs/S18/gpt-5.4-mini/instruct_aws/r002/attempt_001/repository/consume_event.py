import json
from messaging_client import resolve_queue_url, sqs_client
from messaging_models import ConsumeResponse


def consume_event(queue_url=None):
    response = sqs_client().receive_message(
        QueueUrl=resolve_queue_url(queue_url),
        MaxNumberOfMessages=1,
        WaitTimeSeconds=0,
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    return ConsumeResponse(messages=messages)


def main():
    result = consume_event()
    print(json.dumps({"messages": result.messages}))


if __name__ == "__main__":
    main()
