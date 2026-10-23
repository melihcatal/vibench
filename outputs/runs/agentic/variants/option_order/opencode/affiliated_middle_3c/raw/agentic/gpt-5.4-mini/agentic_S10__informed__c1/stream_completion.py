from model_client import get_client, select_model, chat_messages
from model_models import normalize_text


def stream_completion(prompt: str):
    client = get_client()
    model = select_model("stream")
    stream = client.chat.completions.create(
        model=model,
        messages=chat_messages("Stream a helpful completion.", normalize_text(prompt)),
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
