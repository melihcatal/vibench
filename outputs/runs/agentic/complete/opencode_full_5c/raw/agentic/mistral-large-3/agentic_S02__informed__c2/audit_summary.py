from typing import Dict, List, Any
from datetime import datetime
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def summarize_audit_events(audit_events: List[Dict[str, Any]]) -> str:
    """
    Summarize federated-login audit events using Mistral AI.
    Returns a concise summary of login activities, anomalies, and trends.
    """
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=mistral_api_key)

    prompt = (
        "Summarize the following federated-login audit events in a concise manner. "
        "Highlight login activities, anomalies, and trends:\n\n"
        f"{audit_events}"
    )

    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(model="mistral-large-latest", messages=messages)

    return response.choices[0].message.content
