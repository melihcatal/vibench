from messaging_client import get_subscriber, get_subscription_path, decode_message_data
from messaging_models import EventMessage, ConsumeResponse


def consume_event(
    subscription_name: str = None, max_messages: int = 1
) -> ConsumeResponse:
    subscriber = get_subscriber()
    subscription_path = get_subscription_path(subscription_name)

    try:
        response = subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": max_messages,
            }
        )

        if not response.received_messages:
            return ConsumeResponse(
                success=False,
                subscription=subscription_path,
                error="No messages available",
            )

        received = response.received_messages[0]
        message = received.message
        event_data = decode_message_data(message.data)
        event = EventMessage.from_dict(event_data)

        return ConsumeResponse(
            success=True,
            event=event,
            ack_id=received.ack_id,
            subscription=subscription_path,
        )
    except Exception as exc:
        return ConsumeResponse(
            success=False,
            subscription=subscription_path,
            error=str(exc),
        )


def acknowledge_message(ack_id: str, subscription_name: str = None):
    subscriber = get_subscriber()
    subscription_path = get_subscription_path(subscription_name)
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
        }
    )


def nack_message(ack_id: str, subscription_name: str = None):
    subscriber = get_subscriber()
    subscription_path = get_subscription_path(subscription_name)
    subscriber.modify_ack_deadline(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": 0,
        }
    )
