from messaging_client import subscriber_client, subscription_path
from messaging_models import normalize_message, ConsumeResponse


def consume_event(subscription: str, timeout: int = 10) -> ConsumeResponse | None:
    client = subscriber_client()
    response = client.pull(
        request={
            "subscription": subscription_path(subscription),
            "max_messages": 1,
            "return_immediately": True,
        },
        timeout=timeout,
    )
    if not response.received_messages:
        return None
    msg = response.received_messages[0].message
    return ConsumeResponse(
        message_id=msg.message_id,
        data=normalize_message(
            {"data": msg.data.decode("utf-8"), "attributes": dict(msg.attributes)}
        )["data"],
        attributes=dict(msg.attributes),
    )
