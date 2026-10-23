import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def archive_summary(transcript: str, max_tokens: int = 500) -> str:
    """
    Summarize transcription results using Anthropic Claude.
    """
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this transcript:\n\n{transcript}",
            }
        ],
    )
    return message.content[0].text