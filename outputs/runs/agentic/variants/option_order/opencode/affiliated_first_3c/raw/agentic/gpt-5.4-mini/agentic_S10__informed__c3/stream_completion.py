from model_client import get_client, get_config


def stream_completion(prompt: str):
    config = get_config()
    client = get_client()
    stream = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=config.temperature,
        max_tokens=config.max_output_tokens,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
