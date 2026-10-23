import os
from model_client import get_openai_client


def stream_completion(prompt: str) -> str:
    """Stream partial output tokens from OpenAI GPT model."""
    client = get_openai_client()

    full_response = ""

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=100,
        temperature=0.7,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            # In a real application, you might yield or process each chunk
            # For this function, we'll collect and return the full response

    return full_response
