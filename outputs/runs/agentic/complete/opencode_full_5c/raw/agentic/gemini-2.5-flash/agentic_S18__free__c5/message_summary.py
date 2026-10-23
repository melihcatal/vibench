from typing import Dict, Any
from messaging_models import PubsubMessage


def summarize_message_processing(
    message: PubsubMessage, processing_status: str, processing_details: Dict[str, Any]
) -> Dict[str, Any]:
    """Summarizes message processing results.

    This is a local helper function and does not directly integrate with an external provider.
    It aggregates information about a processed message.
    """
    summary = {
        "message_id": message.message_id,
        "status": processing_status,
        "payload_preview": message.data.get("text", str(message.data))[
            :100
        ],  # Take first 100 chars or full data string
        "attributes": message.attributes,
        "processing_details": processing_details,
    }
    return summary
