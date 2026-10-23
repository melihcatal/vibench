from typing import Dict, Any, List, Generator

def build_messages(system: str, user: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]

def normalize_completion(response) -> str:
    return response.choices[0].message.content.strip()

def stream_tokens(client, messages: List[Dict[str, str]], model: str = "gpt-4o-mini") -> Generator[str, None, None]:
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content