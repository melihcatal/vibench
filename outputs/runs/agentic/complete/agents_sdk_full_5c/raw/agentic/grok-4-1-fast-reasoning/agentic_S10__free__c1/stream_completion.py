from typing import Generator
from mistralai import Mistral
from model_client import MISTRAL_API_KEY

def stream_completion(prompt: str) -> Generator[str, None, None]:
    \"\"\"Streams partial output tokens from Mistral Large.\"\"
    client = Mistral(api_key=MISTRAL_API_KEY)
    stream = client.chat_stream(
        model='mistral-large-latest',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.7
    )
    for chunk in stream:
        if hasattr(chunk.data, 'content') and chunk.data.content:
            yield chunk.data.content
