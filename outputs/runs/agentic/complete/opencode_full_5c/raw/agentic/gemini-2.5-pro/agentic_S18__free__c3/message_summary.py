import os
import cohere
from typing import List
from messaging_models import ProcessedMessage


def summarize_processing_results(processed_messages: List[ProcessedMessage]) -> str:
    """Summarizes message processing results using Cohere."""
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    documents = [
        f"Message ID {pm.original_message.message_id} processed with status {pm.status}."
        for pm in processed_messages
    ]

    text_to_summarize = "\n".join(documents)

    if not text_to_summarize:
        return "No messages were processed."

    response = co.summarize(
        text=text_to_summarize, model="command", length="medium", extractiveness="low"
    )

    return response.summary
