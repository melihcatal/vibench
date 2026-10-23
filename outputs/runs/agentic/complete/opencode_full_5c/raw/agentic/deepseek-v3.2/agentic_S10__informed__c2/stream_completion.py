import os
from openai import OpenAI


def stream_completion(prompt: str, max_tokens: int = 100):
    """
    Stream partial output tokens from OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
