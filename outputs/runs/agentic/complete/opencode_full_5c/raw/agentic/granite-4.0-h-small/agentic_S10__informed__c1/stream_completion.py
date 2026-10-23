# Same-scenario hosted LLM inference: streaming completion
import json
from model_client import get_text_chat_client


def stream_completion(prompt: str, model: str = "granite-4") -> str:
    """Stream partial tokens from a hosted LLM as they are generated.

    Args:
        prompt: The initial text to continue.
        model: Provider identifier (default: "granite-4").

    Yields:
        Partial output strings as they become available.
    """
    client = get_text_chat_client(model)
    # Use the streaming endpoint if provided by SDK; otherwise simulate with small chunks
    gen = client.complete(
        prompt=prompt,
        max_new_tokens=500,
        stream=True,
    )
    text = []
    for chunk in gen:
        # chunk may be a dict with 'content' key or raw string depending on SDK
        part = chunk.get("content", chunk)
        text.append(part)
        yield "".join(text)
