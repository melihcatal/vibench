from model_client import build_client, load_config


def stream_completion(prompt: str, provider: str = "openai"):
    config = load_config(provider=provider)
    client = build_client(config)
    stream = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.2,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
