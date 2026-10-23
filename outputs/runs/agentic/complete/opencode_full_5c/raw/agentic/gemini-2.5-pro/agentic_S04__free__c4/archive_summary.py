import os
import anthropic


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes transcription results using Anthropic's Claude model.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following transcript:\n\n{transcript_text}",
            }
        ],
    )
    return message.content[0].text
