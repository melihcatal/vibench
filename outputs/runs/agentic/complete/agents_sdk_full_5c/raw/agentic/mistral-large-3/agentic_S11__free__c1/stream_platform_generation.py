from model_client import get_model_client
from model_models import ModelRequest
from typing import Generator, Dict, Any

def stream_model_generation(prompt: str) -> Generator[Dict[str, Any], None, None]:
    client = get_model_client()
    request = ModelRequest(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    stream = client.chat.completions.create(**request.dict())
    for chunk in stream:
        yield {"chunk": chunk, "content": chunk.choices[0].delta.content}