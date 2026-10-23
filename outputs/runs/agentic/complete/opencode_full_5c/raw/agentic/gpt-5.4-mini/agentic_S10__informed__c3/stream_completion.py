from model_client import get_llm_client, select_chat_model
from model_models import normalize_text


def stream_completion(prompt: str):
    client = get_llm_client()
    model = select_chat_model("streaming")
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": normalize_text(prompt)}],
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
