import os
from model_client import get_llm_client
from model_models import normalize_text

def stream_completion(prompt: str) -> str:
    """Stream partial output tokens from a hosted LLM.
    Uses Anthropic Claude streaming via the Anthropic SDK.
    """
    client = get_llm_client()
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
    )
    partial_output = []
    for chunk in response:
        # chunk.choices[0].delta.content contains token fragments
        token_fragment = chunk.choices[0].delta.content
        if token_fragment:
            partial_output.append(token_fragment)
    return normalize_text(''.join(partial_output))
