import os
from openai import OpenAI


def stream_completion(prompt: str):
    """
    Streams partial output tokens from a hosted LLM (OpenAI).
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.chat.completions.create(
        model="gpt-4o-mini",  # Provider-specific model ID
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
