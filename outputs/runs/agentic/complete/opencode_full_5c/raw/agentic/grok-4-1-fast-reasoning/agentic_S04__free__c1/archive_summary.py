import os
import anthropic
from speech_models import Transcript


def summarize_transcript(transcript: Transcript) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY required")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the key points from this transcript:\n\n{transcript.text}",
            }
        ],
    )
    return message.content[0].text
