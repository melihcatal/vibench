import os
from typing import Any, Iterator, Dict, List
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_completion(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-mini",
    *,
    stream: bool = False,
    response_format: Dict[str, Any] | None = None,
    **kwargs: Any,
) -> str | Iterator[str]:
    if response_format:
        kwargs["response_format"] = response_format
    if stream:
        if response_format is not None:
            raise ValueError("response_format not supported with streaming")
        response = client.chat.completions.create(
            model=model, messages=messages, stream=True, **kwargs
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
    else:
        response = client.chat.completions.create(
            model=model, messages=messages, stream=False, **kwargs
        )
        return response.choices[0].message.content
