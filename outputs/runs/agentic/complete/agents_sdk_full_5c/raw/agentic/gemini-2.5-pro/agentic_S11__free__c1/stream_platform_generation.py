import anthropic
from model_client import ANTHROPIC_API_KEY
from typing import Iterator

def stream_claude_response(prompt: str) -> Iterator[anthropic.types.MessageStreamEvent]:
    """
    Streams the output from an Anthropic Claude model.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    stream = client.messages.stream(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    for event in stream:
        yield event
