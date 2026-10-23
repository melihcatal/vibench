import os
from model_client import HostedLLMClient


def stream_completion(prompt: str, max_tokens: int = 100) -> None:
    """Streams partial tokens from a hosted LLM as they are generated.

    Args:
        prompt (str): The initial prompt to the model.
        max_tokens (int): Maximum number of tokens to generate.
    """
    client = HostedLLMClient()
    model = "gpt-4o-mini"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "stream": True,
    }
    # The client's `stream_generate` yields partial chunks as they arrive
    for chunk in client.stream_generate(payload):
        content = chunk["choices"][0]["delta"].get("content", "")
        if content:
            print(content, end="", flush=True)


if __name__ == "__main__":
    sample = "Write a short poem about sunrise."
    print("Streaming completion:")
    stream_completion(sample, max_tokens=30)
