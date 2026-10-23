import json
from azure.servicebus import ServiceBusMessage
from messaging_client import MessagingClient
from messaging_models import ServiceBusConfig, EventMessage

def consume_event(config: ServiceBusConfig):
    messaging_client = MessagingClient(config)
    receiver = None
    try:
        if config.queue_name:
            receiver = messaging_client.get_queue_receiver()
        elif config.topic_name and config.subscription_name:
            receiver = messaging_client.get_subscription_receiver()
        else:
            raise ValueError("Either queue_name or topic_name and subscription_name must be provided in config.")

        with receiver:
            received_messages = receiver.receive_messages(max_wait_time=5, max_messages=1)
            if received_messages:
                message = received_messages[0]
                payload = json.loads(str(message))
                event_message = EventMessage(event=payload, message_id=message.message_id)
                message.complete()
                return event_message
            else:
                return None
    finally:
        if messaging_client:
            messaging_client.close()
