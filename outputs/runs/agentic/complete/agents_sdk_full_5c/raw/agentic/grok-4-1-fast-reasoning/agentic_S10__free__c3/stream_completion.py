from model_client import get_llm_client
from typing import Generator

def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = get_llm_client()
    messages = [{"role": "user", "content": prompt}]
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        temperature=0.7
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content