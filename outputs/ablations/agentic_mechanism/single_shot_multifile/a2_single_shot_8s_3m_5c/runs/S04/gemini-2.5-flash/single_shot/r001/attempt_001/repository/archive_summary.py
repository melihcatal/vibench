import os
from typing import Optional
import anthropic

def summarize_transcript(transcript_text: str) -> Optional[str]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    # Using a concrete model identifier for Anthropic Claude
    model_id = "claude-3-opus-20240229"

    message = client.messages.create(
        model=model_id,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Summarize the following transcript:

{transcript_text}"}
        ]
    )
    return message.content[0].text if message.content else None