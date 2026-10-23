from .model_client import client


def translate_text(text):
    response = client.completions.create(
        model="claude-v2",
        prompt=f"Translate the following text: {text}",
        max_tokens_to_sample=100,
    )
    return response.completion
