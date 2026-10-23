from messaging_models import EventMessage, ConsumeResult
from messaging_client import consume_message_from_subscription, acknowledge_message


def consume_event(subscription_name: str, timeout: float = 10.0) -> ConsumeResult:
    try:
        result = consume_message_from_subscription(subscription_name, timeout)
        if result is None:
            return ConsumeResult(
                success=False,
                error="No messages available",
                subscription=subscription_name,
            )
        ack_id, message = result
        data = message.data.decode("utf-8")
        event = EventMessage.from_json(data)
        acknowledge_message(subscription_name, ack_id)
        return ConsumeResult(
            message=event,
            success=True,
            subscription=subscription_name,
            ack_id=ack_id,
        )
    except Exception as e:
        return ConsumeResult(
            success=False,
            error=str(e),
            subscription=subscription_name,
        )


if __name__ == "__main__":
    result = consume_event(subscription_name="events-subscription")
    print(result.to_dict())
