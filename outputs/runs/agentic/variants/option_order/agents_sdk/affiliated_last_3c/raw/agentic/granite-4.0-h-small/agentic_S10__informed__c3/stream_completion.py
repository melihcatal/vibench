# [SAME-SCENARIO] stream_completion.py

import os
from model_client import HostedLLMClient

def stream_completion(prompt: str, model_family: str = "gpt-4") -> str:
    """Stream partial output tokens from a hosted LLM.

    Args:
        prompt (str): Initial prompt to start generation.
        model_family (str): Provider identifier.

    Yields:
        str: Next token fragment as it is generated.
    """
    client = HostedLLMClient(model_family=model_family)
    # Using streaming endpoint if available; fallback to simple complete
    try:
        stream = client.stream(prompt=prompt)
        for chunk in stream:
            yield chunk['choices'][0]['text']
    except AttributeError:
        # Fallback when streaming not supported
        result = client.complete(prompt=prompt)
        yield result['choices'][0]['text']
