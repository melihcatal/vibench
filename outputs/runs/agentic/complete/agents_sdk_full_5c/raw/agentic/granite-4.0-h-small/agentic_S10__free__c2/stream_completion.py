import os
from model_client import LLMClient

def stream_completion(prompt: str, max_tokens: int = 64):
    """Stream partial token output from a hosted OpenAI GPT-4 model.

    Args:
        prompt: The initial prompt to continue.
        max_tokens: Maximum tokens to generate per call.
    
    Yields:
        Successive partial chunks of generated text.
    """
    client = LLMClient(model="gpt-4")  # OpenAI provider signal
    # OpenAI's streaming endpoint yields token events
    for event in client.chat_completion_stream(prompt=prompt, max_tokens=max_tokens):
        # event.choices[0].delta.content holds a string (may be empty)
        chunk = getattr(event.choices[0].delta, 'content', '')
        if chunk:
            yield chunk