import os
from openai import OpenAI
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a hosted OpenAI LLM.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION"),
    )

    response_stream = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or another suitable OpenAI model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True,
        max_tokens=300
    )

    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
