from model_client import get_chat_client, select_chat_model, chat_messages


def stream_completion(prompt: str):
    client = get_chat_client()
    model = select_chat_model('streaming')
    stream = client.chat.completions.create(
        model=model,
        messages=chat_messages('Continue the prompt.', prompt),
        temperature=0.4,
        stream=True,
    )
    for chunk in stream:
        choices = getattr(chunk, 'choices', None) or []
        if not choices:
            continue
        delta = getattr(choices[0], 'delta', None)
        if delta and getattr(delta, 'content', None):
            yield delta.content
