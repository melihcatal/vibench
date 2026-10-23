import os
from typing import Optional, Iterator
from model_client import get_llm_client
from model_models import StreamCompletionRequest, StreamCompletionChunk


def stream_completion(
    prompt: str,
    max_tokens: Optional[int] = 150,
    temperature: Optional[float] = 0.7,
    model: Optional[str] = "mistralai/Mistral-7B-Instruct-v0.2"
) -> Iterator[str]:
    """
    Stream partial output tokens from a hosted LLM.
    
    Uses Together.ai's hosted Mistral 7B Instruct v0.2 model.
    """
    client = get_llm_client()
    request = StreamCompletionRequest(
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model,
        stream=True
    )
    response = client.post(
        "https://api.together.xyz/v1/completions",
        json=request.dict(),
        headers={
            "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
            "Content-Type": "application/json"
        },
        stream=True
    )
    for chunk in response.iter_lines():
        if chunk:
            chunk_data = StreamCompletionChunk.parse_raw(chunk.decode('utf-8'))
            if chunk_data.choices and chunk_data.choices[0].text:
                yield chunk_data.choices[0].text