from typing import Generator
from model_client import get_openai_client

def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = get_openai_client()
    model_id = "gpt-4o"
    stream = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content