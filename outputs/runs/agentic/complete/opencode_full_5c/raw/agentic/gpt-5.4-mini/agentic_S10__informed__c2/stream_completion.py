from model_client import get_openai_client, choose_chat_model


def stream_completion(prompt: str, model: str | None = None):
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=choose_chat_model(model),
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
