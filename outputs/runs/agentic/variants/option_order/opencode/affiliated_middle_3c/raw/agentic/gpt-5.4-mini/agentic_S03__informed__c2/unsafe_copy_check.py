import os

from anthropic import Anthropic


def unsafe_copy_check(text: str) -> str:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=[{"role": "user", "content": text}],
    )
    return resp.content[0].text if resp.content else ""
