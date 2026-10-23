import os
from google.cloud import pubsub_v1
from messaging_client import sub_path, ack, consume_one
from messaging_models import deserialize_event, Event

subscriber = pubsub_v1.SubscriberClient()


def consume_event():
    msg = consume_one()
    if msg:
        event = deserialize_event(msg.message.data)
        ack(msg.ack_id)
        print(f"Consumed event {event.id}")
        return event
    print("No message")
    return None
