import os

from model_client import GeminiClient
from model_models import ChatCompletionRequest, ChatPrompt, LLMResponse


def answer_with_context(
    question: str,
    context: str,
    model_name: str = "gemini-pro",
    temperature: float = 0.5,
) -> LLMResponse:
    """Answers a question using provided context with a hosted LLM."""
    prompt_history = [
        ChatPrompt(
            role="user",
            parts=[f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"],
        ),
    ]

    client = GeminiClient()
    request = ChatCompletionRequest(
        history=prompt_history,
        model_name=model_name,
        max_output_tokens=1000,
        temperature=temperature,
    )
    response = client.chat_completion(request)
    return response
