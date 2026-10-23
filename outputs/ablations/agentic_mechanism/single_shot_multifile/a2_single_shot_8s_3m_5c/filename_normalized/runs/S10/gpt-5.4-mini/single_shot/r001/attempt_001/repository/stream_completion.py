from openai import OpenAI
from model_client import get_chat_client, resolve_streaming_model
from model_models import ChatRequest, extract_stream_delta


def stream_completion(prompt: str):
    client = get_chat_client()
    model = resolve_streaming_model()
    request = ChatRequest(
        model=model,
        system_prompt='You are a helpful assistant that produces direct completions.',
        user_prompt=prompt,
        temperature=0.7,
    )
    stream = client.chat.completions.create(stream=True, **request.to_kwargs())
    for chunk in stream:
        delta = extract_stream_delta(chunk)
        if delta:
            yield delta
