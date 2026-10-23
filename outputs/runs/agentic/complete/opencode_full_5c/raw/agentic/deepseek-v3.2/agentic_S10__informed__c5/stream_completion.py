import os
from openai import OpenAI


def stream_completion(prompt: str) -> str:
    """
    Stream partial output tokens from OpenAI's GPT model.
    Returns the full completion after streaming.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    full_response = ""

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
        max_tokens=500,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content

    return full_response
