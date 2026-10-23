from typing import TypedDict, List


class ChatMessage(TypedDict):
    role: str
    content: str


def build_messages(system_prompt: str, user_prompt: str) -> List[ChatMessage]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
