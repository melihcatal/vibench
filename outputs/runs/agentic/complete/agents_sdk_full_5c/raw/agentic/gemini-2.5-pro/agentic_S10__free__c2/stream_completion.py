from typing import Iterable
from model_client import get_cohere_client

def stream_completion(prompt: str) -> Iterable[str]:
    """
    Streams partial tokens from a chat completion.
    """
    client = get_cohere_client()
    
    # The stream=True parameter initiates a streaming connection
    stream = client.chat(
        message=prompt,
        model='command-r',
        stream=True
    )
    
    for event in stream:
        if event.event_type == "text-generation":
            yield event.text
