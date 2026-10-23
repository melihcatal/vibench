from typing import Dict, Any
from messaging_models import PubSubMessage


def summarize_message_processing(message: PubSubMessage) -> Dict[str, Any]:
    """Summarizes the content and attributes of a processed Pub/Sub message.

    Args:
        message: The PubSubMessage object to summarize.

    Returns:
        A dictionary containing a summary of the message.
    """
    summary = {
        "message_id": message.message_id,
        "data_preview": str(message.data)[:100],  # Preview first 100 chars of data
        "attributes": message.attributes,
        "data_type": type(message.data).__name__,
        "processed_at": "<timestamp_placeholder>",  # In a real scenario, this would be a real timestamp
    }
    return summary
