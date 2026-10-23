from typing import Generator
from model_client import get_client

def stream_joke() -> Generator[str, None, None]:
    """
    Streams a joke from an OpenAI model.
    """
    client = get_client()
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Tell me a short, funny joke about programming."}
        ],
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
