from model_client import get_llm_client
from model_models import ChatMessage

def stream_completion(prompt: str):
    client = get_llm_client()
    messages: list[ChatMessage] = [{"role": "user", "content": prompt}]
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        temperature=0.7
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content