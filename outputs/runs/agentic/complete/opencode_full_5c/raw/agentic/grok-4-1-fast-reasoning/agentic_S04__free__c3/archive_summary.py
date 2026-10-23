import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def summarize_transcript(transcript: str) -> str:
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.7,
        messages=[
            {"role": "user", "content": f"Summarize this transcript:\n\n{transcript}"}
        ],
    )
    return message.content[0].text
