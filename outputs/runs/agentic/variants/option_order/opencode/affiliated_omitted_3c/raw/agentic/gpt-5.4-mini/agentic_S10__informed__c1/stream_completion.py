from model_client import create_client, load_settings


def stream_completion(prompt: str):
    settings = load_settings()
    client = create_client()
    with client.messages.stream(
        model=settings.model,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        system="Continue the prompt naturally.",
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text
