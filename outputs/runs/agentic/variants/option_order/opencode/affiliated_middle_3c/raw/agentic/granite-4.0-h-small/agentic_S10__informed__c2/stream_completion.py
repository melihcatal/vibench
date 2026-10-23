# Stream partial tokens from DashScope Qwen API
import os
from dashscope import text
from model_client import get_dashscope_client


def stream_completion(prompt: str, model: str = "qwen-plus"):
    """Iteratively stream token completions from DashScope Qwen model.

    Args:
        prompt (str): The initial prompt.
        model (str): Qwen model identifier (default: "qwen-plus").

    Yields:
        str: Partial token strings as they are generated.
    """
    client = get_dashscope_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        streaming=True,
        temperature=0.7,
    )
    for chunk in response:
        # Each chunk contains partial content in the message
        yield chunk.choices[0].delta.content or ""
