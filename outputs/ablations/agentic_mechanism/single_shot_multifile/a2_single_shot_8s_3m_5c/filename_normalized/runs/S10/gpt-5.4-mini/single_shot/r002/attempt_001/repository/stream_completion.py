from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import stream_messages, stream_text_chunks


def stream_completion(prompt: str):
    client = get_client()
    model = get_model_name("streaming")
    messages = stream_messages(prompt)
    stream = client.chat.completions.create(model=model, messages=messages, temperature=0.7, stream=True)
    return stream_text_chunks(stream)
