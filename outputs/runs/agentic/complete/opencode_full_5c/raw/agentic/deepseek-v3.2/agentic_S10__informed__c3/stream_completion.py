from model_client import ModelClient
from model_models import ChatMessage, StreamChunk


def stream_completion(prompt: str):
    client = ModelClient()

    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content=prompt),
    ]

    stream = client.client.chat.completions.create(
        model="gpt-4o",
        messages=[msg.to_dict() for msg in messages],
        temperature=0.7,
        stream=True,
    )

    for chunk in stream:
        stream_chunk = StreamChunk.from_openai_chunk(chunk)
        if stream_chunk.done:
            break
        if stream_chunk.content:
            yield stream_chunk.content
