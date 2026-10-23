from model_client import get_client, pick_model


def stream_completion(prompt, model=None):
    client = get_client()
    stream = client.chat.completions.create(
        model=pick_model(model),
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for event in stream:
        delta = event.choices[0].delta.content if event.choices else None
        if delta:
            yield delta
