import os
import openai
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    client = openai.OpenAI(
        api_key=openai.api_key,
        base_url=openai.api_base,
    )

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
