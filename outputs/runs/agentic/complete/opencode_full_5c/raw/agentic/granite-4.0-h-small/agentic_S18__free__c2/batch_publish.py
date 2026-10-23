import os
import json
from messaging_client import MessagingClient  # concrete provider: RabbitMQ

# RabbitMQ specifics
EXCHANGE_NAME = os.getenv("RABBIT_EXCHANGE")
ROUTING_KEY = os.getenv("RABBIT_ROUTING_KEY")


def batch_publish(events):
    """Publish a list of JSON events as a batch to RabbitMQ.

    Args:
        events (list[dict]): Events to send.
    """
    client = MessagingClient(exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
    # for event in events:
    #     body = json.dumps(event).encode('utf-8')
    #     client.publish(body)
    # print(f"Batched {len(events)} messages to exchange {EXCHANGE_NAME}")
    print("batch_publish stub: would send all events in batch")
