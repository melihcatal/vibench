from model_client import create_chat_completion
from model_models import GenerationRequest


def summarize_text(
    text: str, max_output_tokens: int = 220, model: str | None = None
) -> dict:
    request = GenerationRequest(
        text=text,
        max_output_tokens=max_output_tokens,
        temperature=0.2,
        model=model,
    )
    result = create_chat_completion(
        request,
        "Summarize the provided text into a concise, faithful summary with the most important facts and decisions.",
    )
    return {
        "provider": result.provider,
        "model": result.model,
        "summary": result.text,
        "usage": result.usage,
        "finish_reason": result.finish_reason,
    }
