from openai import OpenAI
from model_client import get_openai_client, select_chat_model
from model_models import normalize_text


def stream_completion(prompt: str):
    client = get_openai_client()
    model = select_chat_model("streaming")
    stream = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Continue the user's prompt."}, {"role": "user", "content": normalize_text(prompt)}], temperature=0.7, stream=True)
    for event in stream:
        delta = event.choices[0].delta.content if event.choices else None
        if delta:
            yield delta
