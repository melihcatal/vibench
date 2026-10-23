from .model_client import client


def summarize_text(text):
    response = client.completions.create(
        model="claude-v2", prompt=text, max_tokens_to_sample=50
    )
    return response.completion
