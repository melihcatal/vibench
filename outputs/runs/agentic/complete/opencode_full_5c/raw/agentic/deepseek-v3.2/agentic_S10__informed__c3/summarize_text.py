import os
from model_client import ModelClient
from model_models import ChatMessage, CompletionRequest, CompletionResponse


def summarize_text(text: str, max_length: int = 200) -> str:
    client = ModelClient()

    prompt = f"""Please summarize the following text in about {max_length} words or less:

{text}

Summary:"""

    messages = [
        ChatMessage(
            role="system",
            content="You are a helpful assistant that summarizes text concisely.",
        ),
        ChatMessage(role="user", content=prompt),
    ]

    request = CompletionRequest(
        messages=messages, model="gpt-4o-mini", temperature=0.3, max_tokens=300
    )

    response = client.create_completion(
        messages=request.messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    result = CompletionResponse.from_openai_response(response)
    return result.content.strip()
