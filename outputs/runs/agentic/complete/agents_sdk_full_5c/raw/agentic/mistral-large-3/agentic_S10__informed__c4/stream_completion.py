from typing import Iterator, Optional
from model_client import get_llm_client
from model_models import StreamCompletionRequest, StreamCompletionChunk


def stream_completion(
    prompt: str,
    model: Optional[str] = "mistral-tiny"
) -> Iterator[str]:
    """
    Stream partial output tokens from Mistral's chat API.
    """
    client = get_llm_client()
    
    request = StreamCompletionRequest(
        prompt=prompt,
        model=model
    )
    
    stream = client.chat_stream(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}]
    )
    
    for chunk in stream:
        yield StreamCompletionChunk.from_mistral(chunk).text