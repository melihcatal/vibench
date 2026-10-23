from typing import Iterable

from anthropic import Anthropic


def summarize_meeting_chunks(chunks: Iterable[str]) -> str:
    client = Anthropic()
    text = "\n".join(chunks)
    message = client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=256, messages=[{"role": "user", "content": text}])
    return "".join(part.text for part in message.content if hasattr(part, "text"))
