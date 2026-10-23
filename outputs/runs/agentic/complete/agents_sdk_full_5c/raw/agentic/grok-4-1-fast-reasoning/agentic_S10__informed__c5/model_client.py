import os
from typing import List, Dict, Any, Iterator
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable must be set.")

client = OpenAI(api_key=API_KEY)

def create_chat_completion(
    messages: List[Dict[str, Any]],
    model: str = "gpt-4o-mini",
    stream: bool = False,
    **kwargs: Any
) -> Union[Any, Iterator[Any]]:
    kwargs.setdefault("model", model)
    kwargs.setdefault("messages", messages)
    kwargs["stream"] = stream
    return client.chat.completions.create(**kwargs)