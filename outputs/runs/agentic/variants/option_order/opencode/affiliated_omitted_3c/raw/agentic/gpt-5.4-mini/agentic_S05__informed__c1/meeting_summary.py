from anthropic import Anthropic


def summarize_meeting(transcript: str) -> str:
    client = Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=256,
        messages=[{"role": "user", "content": transcript}],
    )
    return "".join(block.text for block in message.content if hasattr(block, "text"))
