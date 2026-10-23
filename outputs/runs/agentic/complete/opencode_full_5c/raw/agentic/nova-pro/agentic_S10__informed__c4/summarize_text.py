import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def summarize_text(text):
    response = client.completions.create(
        model="claude-3-opus-20240229",
        prompt=f"Summarize the following text: {text}",
        max_tokens_to_sample=1024,
    )
    return response.completion
