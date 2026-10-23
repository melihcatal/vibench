from model_client import create_chat_completion
from model_models import GenerationRequest


def answer_with_context(
    question: str, context: str, max_output_tokens: int = 300, model: str | None = None
) -> dict:
    request = GenerationRequest(
        question=question,
        context=context,
        max_output_tokens=max_output_tokens,
        temperature=0.1,
        model=model,
    )
    result = create_chat_completion(
        request,
        "Answer the question using only the supplied context. If the answer is not supported by the context, say that the context does not contain the answer.",
    )
    return {
        "provider": result.provider,
        "model": result.model,
        "answer": result.text,
        "usage": result.usage,
        "finish_reason": result.finish_reason,
    }
