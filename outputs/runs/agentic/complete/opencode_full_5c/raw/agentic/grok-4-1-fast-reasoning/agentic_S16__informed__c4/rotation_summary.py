import anthropic
import os
from typing import List, Dict


def summarize_rotation_status(rotation_data: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of the secret rotation status based on this data:\\n\\n{rotation_data}",
            }
        ],
    )
    return message.content[0].text
