"""Summarize message processing results using OpenAI GPT."""
import os
from typing import Dict, Any
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_message(message_body: Dict[str, Any]) -> str:
    """Summarize message content using OpenAI GPT-3.5-turbo."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Summarize the following message in one sentence."
            },
            {
                "role": "user",
                "content": str(message_body)
            }
        ],
        max_tokens=60
    )
    return response.choices[0].message.content.strip()