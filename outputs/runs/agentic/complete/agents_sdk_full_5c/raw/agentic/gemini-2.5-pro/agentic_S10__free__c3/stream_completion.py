from model_client import get_cohere_client
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a Cohere LLM.

    Args:
        prompt: The prompt to send to the model.

    Yields:
        A stream of text chunks from the model's response.
    """
    cohere_client = get_cohere_client()

    # Provider-specific model ID: command-r
    stream = cohere_client.chat_stream(
        message=prompt,
        model='command-r',
    )

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text
