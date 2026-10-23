import json
from messaging_client import resolve_topic_arn, sns_client, message_attributes
from messaging_models import BatchPublishItem, BatchPublishResponse, PublishResponse, normalize_message_body


def batch_publish(items, topic_arn=None):
    topic = resolve_topic_arn(topic_arn)
    client = sns_client()
    successful = []
    failed = []
    for item in items:
        try:
            normalized = item if isinstance(item, BatchPublishItem) else BatchPublishItem(**item)
            response = client.publish(
                TopicArn=topic,
                Message=normalize_message_body(normalized.payload),
                Subject=normalized.subject or "batch-event",
                MessageAttributes=message_attributes(normalized.message_attributes),
            )
            successful.append(PublishResponse(message_id=response["MessageId"], metadata={k: v for k, v in response.items() if k != "MessageId"}))
        except Exception as exc:
            failed.append({"id": getattr(item, "id", item.get("id") if isinstance(item, dict) else None), "error": str(exc)})
    return BatchPublishResponse(successful=successful, failed=failed)


def main():
    items = json.loads(input())
    result = batch_publish(items)
    print(json.dumps({"successful": [r.__dict__ for r in result.successful], "failed": result.failed}))


if __name__ == "__main__":
    main()
