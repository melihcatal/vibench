from typing import Any, Dict, List, Generator

Message = Dict[str, Any]
Messages = List[Message]

def make_messages(system_prompt: str, user_prompt: str) -> Messages:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def extract_content(response: Any) -> str:
    return response.choices[0].message.content

def stream_tokens(response: Any) -> Generator[str, None, None]:
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta
