from typing import Iterable

from anthropic import Anthropic


def summarize_meeting(chunks: Iterable[str]) -> str:
    client = Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": "Summarize this live meeting transcript:\n"
                + "\n".join(chunks),
            }
        ],
    )
    return message.content[0].text
