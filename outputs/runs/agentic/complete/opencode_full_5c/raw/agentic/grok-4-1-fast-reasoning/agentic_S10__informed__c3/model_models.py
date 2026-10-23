from typing import Dict, Any, List, Union, TypedDict


class ChatMessage(TypedDict):
    role: str
    content: str


class ChatChoice(TypedDict):
    message: ChatMessage


class ChatCompletionResponse(TypedDict):
    choices: List[ChatChoice]


def normalize_completion_response(response: ChatCompletionResponse) -> str:
    return response["choices"][0]["message"]["content"].strip()


def build_chat_messages(
    system_prompt: str = "", user_prompt: str = ""
) -> List[ChatMessage]:
    messages: List[ChatMessage] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})
    return messages
