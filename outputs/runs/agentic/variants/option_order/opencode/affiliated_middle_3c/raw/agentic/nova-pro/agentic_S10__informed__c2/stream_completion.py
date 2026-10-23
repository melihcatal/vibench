from .model_client import client


def stream_completion(text):
    response = client.completions.create(
        model="claude-v2", prompt=text, stream=True, max_tokens_to_sample=100
    )
    for chunk in response:
        yield chunk.completion
