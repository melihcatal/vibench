from typing import List

from anthropic import Anthropic


def moderation_summary(decisions: List[str]) -> str:
    client = Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": "Summarize these moderation decisions: "
                + " | ".join(decisions),
            }
        ],
    )
    return message.content[0].text
