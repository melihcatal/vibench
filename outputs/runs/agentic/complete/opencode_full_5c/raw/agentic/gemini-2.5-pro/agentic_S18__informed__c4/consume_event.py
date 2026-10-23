import json
from google.api_core import exceptions
from messaging_client import (
    get_subscriber_client,
    get_subscription_path,
    PROJECT_ID,
    SUBSCRIPTION_ID,
)


def consume_one_message():
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscriber, PROJECT_ID, SUBSCRIPTION_ID)

    ack_ids = []
    message_payloads = []

    try:
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": 1}
        )

        for received_message in response.received_messages:
            message_payloads.append(
                json.loads(received_message.message.data.decode("utf-8"))
            )
            ack_ids.append(received_message.ack_id)

        if ack_ids:
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
            print(f"Received and acknowledged {len(message_payloads)} message(s).")
        else:
            print("No messages received.")
            return None

        return message_payloads[0] if message_payloads else None

    except exceptions.NotFound:
        print(f"Subscription not found: {subscription_path}")
        return None
