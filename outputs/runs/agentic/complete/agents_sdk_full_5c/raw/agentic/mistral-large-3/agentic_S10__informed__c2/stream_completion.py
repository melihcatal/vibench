import os
from typing import Iterator
from model_client import get_dashscope_client
from model_models import StreamingRequest, StreamingResponseChunk

def stream_completion(
    prompt: str,
    model: str = "qwen-turbo",
    temperature: float = 0.7,
) -> Iterator[str]:
    """
    Stream partial output tokens from DashScope Qwen model.
    
    Args:
        prompt: Input prompt for completion.
        model: Model identifier (e.g., "qwen-turbo", "qwen-plus").
        temperature: Sampling temperature.
    
    Yields:
        Partial output tokens as they are generated.
    """
    client = get_dashscope_client()
    
    request = StreamingRequest(
        model=model,
        prompt=prompt,
        temperature=temperature,
    )
    
    for chunk in client.stream_model(request):
        yield StreamingResponseChunk(**chunk).token