from typing import Iterator
from model_client import get_model_client
from model_models import ChatMessage

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams a completion for the given prompt from an OpenAI model.
    """
    client = get_model_client()
    
    messages = [
        ChatMessage(role="user", content=prompt)
    ]
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[m.to_dict() for m in messages],
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        print(f"An error occurred: {e}")
        yield f"An error occurred during streaming: {e}"
