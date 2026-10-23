from model_client import client


def stream_completion(prompt):
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in response:
        yield chunk.content
