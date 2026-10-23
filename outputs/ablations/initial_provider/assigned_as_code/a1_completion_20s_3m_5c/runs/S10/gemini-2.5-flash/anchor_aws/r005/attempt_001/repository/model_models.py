from typing import TypedDict, List, Dict, Any

class BedrockMessageContent(TypedDict):
    text: str

class BedrockMessage(TypedDict):
    role: str  # "user" or "assistant"
    content: List[BedrockMessageContent]

class BedrockConverseRequest(TypedDict):
    modelId: str
    messages: List[BedrockMessage]
    inferenceConfig: Dict[str, Any]

class BedrockConverseResponseContent(TypedDict):
    text: str

class BedrockConverseResponseMessage(TypedDict):
    content: List[BedrockConverseResponseContent]

class BedrockConverseOutput(TypedDict):
    message: BedrockConverseResponseMessage

class BedrockConverseResponse(TypedDict):
    output: BedrockConverseOutput
