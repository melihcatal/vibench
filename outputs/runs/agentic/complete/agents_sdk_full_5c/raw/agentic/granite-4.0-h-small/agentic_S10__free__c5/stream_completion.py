import asyncio, json
import openai
from model_client import get_openai_client

def stream_completion(prompt: str, model: str = "gpt-4o-mini"):
    """Stream partial output tokens from OpenAI GPT model.
\n    Args:\n        prompt: The generation prompt.\n        model: Model identifier (default gpt-4o-mini).\n    Yields:\n        Partial response chunks as strings.\n    """
    client = get_openai_client()
    response = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
    )
    for chunk in response:
        # chunk.choices[0].delta contains the streamed content
        delta = chunk.choices[0].delta
        content = getattr(delta, 'content', '')
        if content:
            yield content