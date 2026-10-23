import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def stream_completion(prompt):
    response = client.completions.create(
        model="claude-3-opus-20240229",
        prompt=prompt,
        max_tokens_to_sample=1024,
        stream=True,
    )
    for chunk in response:
        yield chunk.completion
