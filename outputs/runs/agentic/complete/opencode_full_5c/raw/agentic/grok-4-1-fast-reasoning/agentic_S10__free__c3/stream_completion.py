from typing import Generator
from model_client import get_groq_client


def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = get_groq_client()
    stream = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta
