import os
from model_client import get_llm_client
from model_models import InferenceResponse

def stream_completion(prompt: str, model_family: str = "gpt-4"):
    """Stream partial output tokens from a hosted LLM.

    Args:
        prompt: The initial prompt to start generation.
        model_family: LLM family/model identifier (default: "gpt-4").

    Yields:
        Chunks of generated text as they become available.
    """
    client = get_llm_client(model_family)
    payload = {
        "model": model_family,
        "prompt": prompt,
        "max_tokens": 500,
        "stream": True,
        "temperature": 0.7,
    }
    # Assume the client returns an iterable of response chunks with a 'content' field
    for chunk in client.stream_chat(payload):
        # Each chunk may contain partial content; concatenate as needed
        yield chunk.choices[0].message.content.strip()
