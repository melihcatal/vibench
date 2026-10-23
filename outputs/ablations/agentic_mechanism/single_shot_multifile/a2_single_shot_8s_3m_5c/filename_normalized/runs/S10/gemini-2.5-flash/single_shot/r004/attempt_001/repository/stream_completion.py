from model_client import get_openai_client
from model_models import ChatMessage, StreamChunk
from typing import Generator

def stream_completion(prompt: str, model_id: str = "gpt-4o") -> Generator[StreamChunk, None, None]:
    client = get_openai_client()
    messages = [
        ChatMessage(role="user", content=prompt)
    ]
    try:
        stream = client.chat.completions.create(
            model=model_id,
            messages=[m.to_dict() for m in messages],
            stream=True,
            max_tokens=500,
            temperature=0.7
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                yield StreamChunk(delta_content=chunk.choices[0].delta.content)
    except Exception as e:
        yield StreamChunk(delta_content=f"Error during streaming: {e}")
