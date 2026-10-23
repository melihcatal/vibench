from messaging_client import get_sns_client
from messaging_models import BatchPublishRequest, BatchPublishResponse, normalize_payload


def batch_publish(request: BatchPublishRequest) -> BatchPublishResponse:
    sns = get_sns_client()
    successful = []
    failed = []
    for entry in request.entries:
        try:
            response = sns.publish(
                TopicArn=request.topic_arn,
                Message=normalize_payload(entry.get("payload")),
                MessageAttributes={
                    key: {"DataType": "String", "StringValue": value}
                    for key, value in entry.get("attributes", {}).items()
                },
            )
            successful.append({"id": entry.get("id"), "message_id": response["MessageId"]})
        except Exception as exc:
            failed.append({"id": entry.get("id"), "error": str(exc)})
    return BatchPublishResponse(successful=successful, failed=failed, provider="aws-sns")
