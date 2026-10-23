from model_client import create_client, model_name


def stream_completion(prompt: str):
    client = create_client()
    stream = client.chat.completions.create(
        model=model_name(),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if getattr(delta, "content", None):
            yield delta.content
