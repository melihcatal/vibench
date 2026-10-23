from model_client import get_client, get_model_name


def stream_completion(prompt: str):
    client = get_client()
    stream = client.chat.completions.create(
        model=get_model_name(),
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
