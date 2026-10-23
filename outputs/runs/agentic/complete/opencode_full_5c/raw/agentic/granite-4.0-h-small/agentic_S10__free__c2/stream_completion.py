# stream_completion.py
# [SAME-SCENARIO]
"""Streams incremental tokens from a hosted LLM as they are generated."""

from model_client import LLMClient


async def stream_completion(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Streams tokens from the hosted model and yields them progressively.

    Args:
        prompt (str): The initial prompt text.
        model (str): Identifier of the hosted model to use.
    Yields:
        str: The next token or partial token as it is generated.
    """
    client = LLMClient(model=model)
    async for chunk in client.chat_stream(
        messages=[{"role": "user", "content": prompt}]
    ):
        # chunk['choices'][0]['delta']['content'] can be None or partial string
        delta = chunk["choices"][0]["delta"].get("content", "")
        if delta:
            yield delta


# Example usage (run in an async context):
# tokens = await stream_completion("Write a short story about a robot.")
# print(''.join(tokens))
