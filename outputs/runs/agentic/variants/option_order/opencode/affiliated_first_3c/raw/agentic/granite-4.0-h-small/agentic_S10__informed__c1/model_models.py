from typing import TypedDict, List, Any


# Request type for the inference client
class ChatMessage(TypedDict):
    role: str  # "user" or "assistant"
    content: str


# Normalized response shape from the inference client
class TextChatResponse(TypedDict):
    choices: List[dict]


# Helper to format a list of ChatMessage into the dict expected by the SDK
# (All the SDK already expects this format, but this normalizer can be extended if the SDK changes.)
def format_chat_request(messages: List[ChatMessage]) -> dict:
    return {"messages": messages}


# Helper to extract the generated text from a raw SDK response
# The raw response is assumed to be the TextChatResponse format shown above
# This normalization makes downstream code independent of the exact SDK structure.
def extract_generated_text(response: TextChatResponse) -> str:
    # Assume the first choice contains the assistant's message
    return response["choices"][0]["message"]["content"]
