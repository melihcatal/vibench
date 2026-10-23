import boto3


def message_summary(messages):
    summaries = []
    for message in messages:
        summaries.append(
            {
                "message_id": message["MessageId"],
                "body": message["Body"],
                "attributes": message.get("MessageAttributes", {}),
            }
        )
    return summaries
