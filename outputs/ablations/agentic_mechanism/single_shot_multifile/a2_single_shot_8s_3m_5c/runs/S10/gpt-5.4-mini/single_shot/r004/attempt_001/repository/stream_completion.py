from typing import Iterator, Optional
from model_client import get_openai_client, select_text_model


def stream_completion(prompt: str, model: Optional[str] = None) -> Iterator[str]:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="streaming")
    stream = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta else None
        if delta:
            yield delta
