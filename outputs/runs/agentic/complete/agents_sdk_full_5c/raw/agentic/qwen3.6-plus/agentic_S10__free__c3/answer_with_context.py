"""
Calls a hosted LLM (OpenAI GPT-4o) to answer a question using provided context.

Provider: OpenAI (api.openai.com)
Model family: gpt-4o
"""

from typing import Optional

from model_client import (
    get_sync_client,
    select_model_family,
    build_system_message,
    build_user_message,
    configure_completion_kwargs,
)
from model_models import (
    QARequest,
    QAResponse,
    extract_text_from_openai_response,
    extract_token_usage,
)

OPENAI_API_HOST = "api.openai.com"
OPENAI_MODEL_FAMILY = "gpt-4o"


def build_qa_instruction(request: QARequest) -> str:
    """Build the system instruction for context-based QA."""
    return (
        f"You are a question answering assistant powered by OpenAI's {OPENAI_MODEL_FAMILY} model family. "
        f"Answer the user's question using ONLY the provided context. "
        f"If the answer cannot be determined from the context, say so explicitly. "
        f"Keep the answer concise and factual. "
        f"Maximum answer length: {request.max_answer_length} words."
    )


def answer_with_context(
    request: QARequest,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> QAResponse:
    """
    Answer a question using provided context via OpenAI GPT-4o hosted LLM.

    Args:
        request: QARequest with question and context.
        model: Optional explicit OpenAI model identifier.
        temperature: Sampling temperature (lower for factual QA).

    Returns:
        QAResponse containing the answer and metadata.
    """
    selected_model = model or select_model_family("qa")

    system_msg = build_system_message(build_qa_instruction(request))
    user_content = f"Context:\n{request.context}\n\nQuestion: {request.question}"
    user_msg = build_user_message(user_content)

    client = get_sync_client()

    kwargs = configure_completion_kwargs(
        messages=[system_msg, user_msg],
        model=selected_model,
        temperature=temperature,
        max_tokens=request.max_answer_length * 2,
    )

    completion = client.chat.completions.create(**kwargs)

    answer = extract_text_from_openai_response(completion)
    usage = extract_token_usage(completion)

    return QAResponse(
        answer=answer,
        model_used=selected_model,
        token_usage=usage,
    )


if __name__ == "__main__":
    sample = QARequest(
        question="What year was the company founded?",
        context="Acme Corp was established in 1987 by Dr. Jane Doe in Silicon Valley.",
        max_answer_length=100,
    )
    result = answer_with_context(sample)
    print(f"Model: {result.model_used}")
    print(f"Answer: {result.answer}")
