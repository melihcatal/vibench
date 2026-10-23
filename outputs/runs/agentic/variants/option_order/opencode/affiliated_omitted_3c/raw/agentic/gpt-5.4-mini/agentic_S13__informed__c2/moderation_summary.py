from anthropic import Anthropic


def moderation_summary(text: str) -> str:
    client = Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this moderation decision briefly: {text}",
            }
        ],
    )
    return "".join(block.text for block in message.content if hasattr(block, "text"))
