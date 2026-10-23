import os
from typing import Optional, Iterator
from model_client import get_llm_client
from model_models import CompletionRequest, CompletionChunk


def stream_completion(
    prompt: str,
    max_tokens: int = 100,
    temperature: float = 0.7,
    model: Optional[str] = "meta-llama/Meta-Llama-3-8B-Instruct"
) -> Iterator[str]:
    """
    Stream partial output tokens from a hosted LLM.
    Uses Together.ai's hosted Llama 3 8B Instruct model by default.
    """
    client = get_llm_client()
    request = CompletionRequest(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model,
        stream=True
    )
    response = client.post(
        "/inference",
        json=request.dict(),
        headers={
            "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
            "Accept": "text/event-stream"
        },
        stream=True
    )
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            chunk = CompletionChunk(**{
                "text": line.decode("utf-8").replace("data: ", "")
            })
            yield chunk.text