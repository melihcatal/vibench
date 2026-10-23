import os
from model_client import get_chat_client
from model_models import format_chat_response

def stream_completion(prompt: str, model: str = "gpt-4o"):
    """Stream partial output tokens from a hosted LLM.

    Yields token strings as they are generated.
    """
    client = get_chat_client(model)
    response = client.chat(
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=1024,
    )
    for chunk in response:
        # chunk contains a 'choices' list; we take the first one
        text = chunk.choices[0].delta.content or ""
        if text:
            yield text
