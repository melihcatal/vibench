from google.cloud import pubsub_v1
from messaging_client import DEAD_LETTER_TOPIC_PATH
from messaging_models import PubSubMessage


def send_to_dead_letter(message: PubSubMessage) -> str:
    publisher = pubsub_v1.PublisherClient()
    future = publisher.publish(
        DEAD_LETTER_TOPIC_PATH, message.data, **message.attributes
    )
    message_id = future.result()
    return message_id
