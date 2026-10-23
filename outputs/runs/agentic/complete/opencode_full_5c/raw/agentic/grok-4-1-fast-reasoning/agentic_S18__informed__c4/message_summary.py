import os
import json
from typing import Dict, Any
from anthropic import Anthropic
from messaging_models import PubSubMessage


def summarize_message(msg: PubSubMessage) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required.")
    client = Anthropic(api_key=api_key)
    text = json.dumps(msg.data)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the key points of this message processing result: {text}",
            }
        ],
    )
    return message.content[0].text
