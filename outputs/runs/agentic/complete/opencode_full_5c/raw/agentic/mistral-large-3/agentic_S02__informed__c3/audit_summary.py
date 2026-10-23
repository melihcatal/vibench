from typing import Dict, Any, List
import os
from datetime import datetime
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Mistral Chat API
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = "mistral-large-latest"


def audit_summary(events: List[Dict[str, Any]]) -> str:
    """Summarize federated-login audit events using Mistral."""
    client = MistralClient(api_key=MISTRAL_API_KEY)

    prompt = (
        "Summarize the following federated login audit events in a concise report. "
        "Include key metrics, anomalies, and recommendations:\n\n"
        f"{events}"
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model=MISTRAL_MODEL, messages=messages)

    return response.choices[0].message.content
