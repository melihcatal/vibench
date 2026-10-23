import json
from typing import List

from messaging_client import sns_client
from messaging_models import normalize_payload


def batch_publish(topic_arn: str, messages: List[dict]) -> dict:
    client = sns_client()
    results = []
    for item in messages:
        response = client.publish(TopicArn=topic_arn, Message=normalize_payload(item.get("message", {})), Subject=item.get("subject", ""), MessageAttributes=item.get("attributes", {}))
        results.append({"id": item.get("id"), "message_id": response["MessageId"]})
    return {"results": results}


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(batch_publish(data["topic_arn"], data.get("messages", []))))


if __name__ == "__main__":
    main()
