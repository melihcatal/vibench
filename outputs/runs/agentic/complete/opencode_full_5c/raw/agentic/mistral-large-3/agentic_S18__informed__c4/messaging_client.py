from google.cloud import pubsub_v1
import os
from typing import Union


def get_messaging_client(
    client_class: Union[
        type(pubsub_v1.PublisherClient), type(pubsub_v1.SubscriberClient)
    ],
) -> Union[pubsub_v1.PublisherClient, pubsub_v1.SubscriberClient]:
    """
    Provides a configured Google Cloud Pub/Sub client.

    Args:
        client_class: The Google Cloud Pub/Sub client class to instantiate.

    Returns:
        Configured Google Cloud Pub/Sub client instance.
    """
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")

    return client_class()
