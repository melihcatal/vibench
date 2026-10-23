from google.cloud import pubsub_v1


def create_pubsub_message(data, attributes=None):
    """Create a Pub/Sub message."""
    message = pubsub_v1.types.PubsubMessage(data=data, attributes=attributes)
    return message


def parse_pubsub_message(message):
    """Parse a Pub/Sub message."""
    data = message.data
    attributes = message.attributes
    return data, attributes


def normalize_pubsub_message(message):
    """Normalize a Pub/Sub message."""
    data, attributes = parse_pubsub_message(message)
    normalized_message = {
        'data': data,
        'attributes': attributes,
    }
    return normalized_message