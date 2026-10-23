import boto3


def summarize_messages(messages):
    summaries = []
    for message in messages:
        summaries.append(
            {
                "message_id": message["MessageId"],
                "body": message["Body"],
                "attributes": message["MessageAttributes"],
            }
        )
    return summaries
