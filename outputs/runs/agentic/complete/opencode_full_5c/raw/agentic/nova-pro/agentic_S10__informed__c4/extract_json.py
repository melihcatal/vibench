import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_json(text):
    response = client.completions.create(
        model="claude-3-opus-20240229",
        prompt=f"Extract structured JSON from the following text: {text}",
        max_tokens_to_sample=1024,
    )
    return response.completion
