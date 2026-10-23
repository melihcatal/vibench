from typing import Dict, List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def moderation_summary(decisions: List[Dict]) -> str:
    """Summarize moderation decisions using Mistral Chat API."""
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    decision_texts = "\n".join(
        [
            f"Text: {d['text']}\nDecision: {'Allowed' if d['allowed'] else 'Blocked'}\nReason: {d.get('reason', 'N/A')}"
            for d in decisions
        ]
    )

    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize the following moderation decisions in a concise report:\n\n{decision_texts}",
        )
    ]

    response = client.chat(
        model="mistral-large-latest",
        messages=messages,
    )
    return response.choices[0].message.content
