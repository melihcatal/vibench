from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from typing import Dict, Any, List


def message_summary(messages: List[Dict[str, Any]]) -> str:
    """
    Summarizes message processing results using Mistral Chat API.

    Args:
        messages: List of dictionaries containing message data.

    Returns:
        Summary of message processing results.
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    message_texts = [
        f"Message ID: {msg.get('event_id', 'N/A')}, Type: {msg.get('event_type', 'N/A')}, Data: {msg.get('data', {})}"
        for msg in messages
    ]

    prompt = (
        "Summarize the following message processing results in a concise manner:\n"
        f"{chr(10).join(message_texts)}"
    )

    chat_response = client.chat(
        model="mistral-large-latest",
        messages=[ChatMessage(role="user", content=prompt)],
    )

    return chat_response.choices[0].message.content
