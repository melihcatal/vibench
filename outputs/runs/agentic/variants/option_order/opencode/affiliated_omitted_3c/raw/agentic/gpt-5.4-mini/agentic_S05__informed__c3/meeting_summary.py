from anthropic import Anthropic


def summarize_meeting(transcript_chunks: list[str]) -> str:
    client = Anthropic(api_key="")
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=[{"role": "user", "content": "\n".join(transcript_chunks)}],
    )
    return message.content[0].text
