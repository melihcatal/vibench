import json
from typing import Any, Dict

from messaging_client import sns_client
from messaging_models import PublishRequest, PublishResponse, normalize_payload


def publish_event(topic_arn: str, message: Any, subject: str = None, attributes: Dict[str, Dict[str, str]] = None) -> PublishResponse:
    client = sns_client()
    request = PublishRequest(topic_arn=topic_arn, message=message, subject=subject, attributes=attributes)
    kwargs = {"TopicArn": request.topic_arn, "Message": normalize_payload(request.message)}
    if request.subject:
        kwargs["Subject"] = request.subject
    if request.attributes:
        kwargs["MessageAttributes"] = request.attributes
    response = client.publish(**kwargs)
    return PublishResponse(message_id=response["MessageId"], request_id=response.get("ResponseMetadata", {}).get("RequestId"))


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    result = publish_event(data["topic_arn"], data.get("message", {}), data.get("subject"), data.get("attributes"))
    print(json.dumps(result.__dict__))


if __name__ == "__main__":
    main()
