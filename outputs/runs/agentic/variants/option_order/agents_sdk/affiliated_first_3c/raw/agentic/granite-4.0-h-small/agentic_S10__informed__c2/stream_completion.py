import os
from model_client import get_llm_client
from model_models import sanitize_response

def stream_completion(prompt: str, max_tokens: int = 100):
    """Stream partial output tokens from a hosted LLM (OpenAI GPT-3.5 Turbo).\n    Yields a generator of token strings as they are generated.
    """
    client = get_llm_client()
    response = client.chat_completion_stream(messages=[{"role": "user", "content": prompt}], max_tokens=max_tokens)
    for chunk in response:
        # assuming chunk contains raw token string under 'choices[0].delta.content'
        delta = chunk.get('choices', [{}])[0].get('delta', {})
        content = delta.get('content', '')
        yield sanitize_response(content)
