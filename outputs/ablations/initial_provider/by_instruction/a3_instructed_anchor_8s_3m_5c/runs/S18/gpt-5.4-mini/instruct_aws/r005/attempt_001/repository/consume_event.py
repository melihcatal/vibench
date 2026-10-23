import json

from messaging_client import sqs_client
from messaging_models import ConsumeResponse


def consume_event(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 0) -> ConsumeResponse:
    client = sqs_client()
    response = client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=max_messages, WaitTimeSeconds=wait_time_seconds, MessageAttributeNames=["All"], AttributeNames=["All"])
    return ConsumeResponse(messages=response.get("Messages", []))


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    result = consume_event(data["queue_url"], data.get("max_messages", 1), data.get("wait_time_seconds", 0))
    print(json.dumps({"messages": result.messages}))


if __name__ == "__main__":
    main()
