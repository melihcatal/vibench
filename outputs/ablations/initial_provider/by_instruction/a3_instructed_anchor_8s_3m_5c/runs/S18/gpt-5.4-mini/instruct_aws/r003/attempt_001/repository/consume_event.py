from messaging_client import get_settings, sqs_client


def consume_event():
    settings = get_settings()
    response = sqs_client().receive_message(
        QueueUrl=settings["queue_url"],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1,
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    return messages[0] if messages else None
