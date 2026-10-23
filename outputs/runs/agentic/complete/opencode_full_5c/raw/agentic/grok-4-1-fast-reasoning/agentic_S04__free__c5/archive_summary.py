import os
import anthropic
from typing import Dict, Any

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def archive_summary(transcript: str) -> str:
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this transcript, highlighting key points and decisions:\\n\\n{transcript}",
            }
        ],
    )
    return message.content[0].text
