import os
from model_client import get_llm_client
from model_models import LLMResponse

def stream_completion(prompt: str, model_name: str = "gpt-4o-mini"):
    """Stream partial output tokens from a hosted LLM via OpenAI provider.
    Uses streaming endpoint to yield tokens as they are generated.
    Identifies provider via SDK import and model identifier.
    """
    client = get_llm_client(model_name)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        stream=True,
    )
    for chunk in response:
        content = chunk.choices[0].delta.get('content', '')
        if content:
            yield content
