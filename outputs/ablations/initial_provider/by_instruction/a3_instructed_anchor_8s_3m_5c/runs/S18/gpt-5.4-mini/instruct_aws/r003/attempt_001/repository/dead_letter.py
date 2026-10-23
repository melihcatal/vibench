from messaging_client import get_settings, sqs_client


def dead_letter(message):
    settings = get_settings()
    return sqs_client().send_message(
        QueueUrl=settings["dead_letter_queue_url"],
        MessageBody=message.get("Body", ""),
        MessageAttributes=message.get("MessageAttributes", {}),
    )
