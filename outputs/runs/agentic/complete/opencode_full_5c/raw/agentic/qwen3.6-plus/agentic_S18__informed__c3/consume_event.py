import json
import os
from messaging_models import PubSubEvent, PubSubMessage, ConsumeResult
from messaging_client import subscription_path, pull_message, acknowledge_message


def consume_event(
    auto_ack: bool = True,
) -> ConsumeResult:
    subscription = subscription_path()

    try:
        received = pull_message(subscription, max_messages=1)
        if not received:
            return ConsumeResult(
                message=None,
                acknowledged=False,
                error="No messages available",
            )

        received_message = received[0]
        msg = received_message.message
        pubsub_msg = PubSubMessage(
            message_id=msg.message_id,
            data=msg.data,
            attributes=dict(msg.attributes),
            publish_time=str(msg.publish_time) if msg.publish_time else None,
        )

        if auto_ack:
            acknowledge_message(subscription, received_message.ack_id)
            return ConsumeResult(
                message=pubsub_msg,
                acknowledged=True,
            )
        else:
            return ConsumeResult(
                message=pubsub_msg,
                acknowledged=False,
            )

    except Exception as exc:
        return ConsumeResult(
            message=None,
            acknowledged=False,
            error=str(exc),
        )


def main():
    result = consume_event()
    print(json.dumps(result.to_dict(), default=str))


if __name__ == "__main__":
    main()
