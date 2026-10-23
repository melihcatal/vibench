import json
from model_client import create_client


def stream_completion(prompt: str, model: str = "gpt-4o-mini"):
    """Stream partial output tokens from a hosted LLM.

    Args:
        prompt (str): The prompt to complete.
        model (str): The model family to use (default: gpt-4o-mini).

    Yields:
        str: Partial generated token sequences as they become available.
    """
    client = create_client(model)
    # OpenAI-compatible client example; adapt for your provider's streaming API
    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in response.choices[0].delta.content or []:
        yield chunk
