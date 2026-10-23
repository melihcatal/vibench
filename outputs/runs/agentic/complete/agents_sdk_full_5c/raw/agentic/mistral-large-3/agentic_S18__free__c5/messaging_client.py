import os
from google.cloud import pubsub_v1

def get_pubsub_client(client_type: str = "publisher") -> pubsub_v1.PublisherClient | pubsub_v1.SubscriberClient:
    if client_type == "publisher":
        return pubsub_v1.PublisherClient()
    elif client_type == "subscriber":
        return pubsub_v1.SubscriberClient()
    else:
        raise ValueError("Invalid client_type. Use 'publisher' or 'subscriber'.")