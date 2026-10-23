import json

from messaging_client import sqs_client


def send_to_dead_letter(queue_url: str, payload: dict) -> str:
    client = sqs_client()
    response = client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(payload, separators=(",", ":"), sort_keys=True))
    return response["MessageId"]


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    print(json.dumps({"message_id": send_to_dead_letter(data["queue_url"], data.get("payload", {}))}))


if __name__ == "__main__":
    main()
