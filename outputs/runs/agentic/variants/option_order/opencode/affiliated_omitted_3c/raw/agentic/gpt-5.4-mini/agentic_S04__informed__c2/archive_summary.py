import os
from anthropic import Anthropic


def archive_summary(transcript_text: str):
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[{"role": "user", "content": f"Summarize this transcript for archival use:
{transcript_text}"}],
    )
    return {"summary": message.content[0].text}
