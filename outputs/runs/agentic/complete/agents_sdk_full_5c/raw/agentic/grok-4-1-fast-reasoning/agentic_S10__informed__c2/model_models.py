from typing import Any, Dict, List, TypedDict

class ChatMessage(TypedDict):
    role: str
    content: str

def build_messages(system_prompt: str, user_prompt: str) -> List[ChatMessage]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

def normalize_chat_response(response: Any) -> str:
    return response.choices[0].message.content.strip()