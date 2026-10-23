import json

from messaging_client import create_servicebus_client, load_config, message_body_text


def consume_one_message() -> dict:
    config = load_config()
    with create_servicebus_client() as client:
        receiver = client.get_subscription_receiver(topic_name=config.topic_name, subscription_name=config.subscription_name) if config.subscription_name else client.get_queue_receiver(queue_name=config.queue_name)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return {"received": False}
            message = messages[0]
            body = message_body_text(message)
            receiver.complete_message(message)
            return {"received": True, "body": body, "message_id": getattr(message, "message_id", None)}


if __name__ == "__main__":
    print(json.dumps(consume_one_message()))
