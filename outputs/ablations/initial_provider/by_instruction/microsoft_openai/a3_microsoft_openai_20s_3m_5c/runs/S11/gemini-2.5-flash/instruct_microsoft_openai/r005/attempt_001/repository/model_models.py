from typing import List, Dict, Any, TypedDict

class Message(TypedDict):
    role: str
    content: str

class CompletionRequest(TypedDict):
    messages: List[Message]
    model: str
    temperature: float
    max_tokens: int

class CompletionChoice(TypedDict):
    index: int
    message: Message
    finish_reason: str

class CompletionUsage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class CompletionResponse(TypedDict):
    id: str
    object: str
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: CompletionUsage

def normalize_openai_response(response: Any) -> CompletionResponse:
    """Normalizes an Azure OpenAI SDK response object into a consistent dictionary format."""
    # This function demonstrates how to extract and normalize key fields
    # from the OpenAI SDK response object into a predefined local structure.
    # In a real application, more detailed normalization might be required.
    normalized_choices = []
    for choice in response.choices:
        normalized_choices.append({
            "index": choice.index,
            "message": {"role": choice.message.role, "content": choice.message.content},
            "finish_reason": choice.finish_reason,
        })

    normalized_usage = response.usage.model_dump() if response.usage else None

    return {
        "id": response.id,
        "object": response.object,
        "created": response.created,
        "model": response.model,
        "choices": normalized_choices,
        "usage": normalized_usage,
    }
