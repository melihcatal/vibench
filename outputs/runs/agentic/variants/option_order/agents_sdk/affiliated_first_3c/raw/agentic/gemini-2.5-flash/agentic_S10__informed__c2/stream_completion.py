import os
from typing import Generator, Dict, Any
from model_client import get_gemini_client

def stream_completion(prompt: str, model_id: str = 'gemini-pro') -> Generator[str, None, None]:
    client = get_gemini_client()
    response_stream = client.generate_content(prompt, stream=True)
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

