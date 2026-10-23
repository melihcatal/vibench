from .model_client import client


def extract_json(text):
    response = client.completions.create(
        model="claude-v2",
        prompt=f"Extract JSON from the following text: {text}",
        max_tokens_to_sample=100,
    )
    return response.completion
