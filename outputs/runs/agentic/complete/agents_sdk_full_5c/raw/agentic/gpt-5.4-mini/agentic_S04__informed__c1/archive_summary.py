import os

from anthropic import Anthropic


MODEL_ID = "claude-3-5-sonnet-20240620"


def archive_summary(transcript_text: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is required")
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=MODEL_ID,
        max_tokens=400,
        temperature=0.2,
        messages=[
            {"role": "user", "content": f"Summarize this transcription result for archival purposes:\n\n{transcript_text}"}
        ],
    )
    return "".join(block.text for block in message.content if hasattr(block, "text"))
