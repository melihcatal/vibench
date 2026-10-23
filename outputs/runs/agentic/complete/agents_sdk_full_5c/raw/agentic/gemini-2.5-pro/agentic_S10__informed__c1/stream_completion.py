from typing import Iterator
from model_client import get_anthropic_client

MODEL_NAME = "claude-3-5-sonnet-20240620"

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from the Anthropic API.
    """
    client = get_anthropic_client()

    try:
        with client.messages.stream(
            model=MODEL_NAME,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as e:
        print(f"An error occurred during streaming: {e}")
        yield "An error occurred."
