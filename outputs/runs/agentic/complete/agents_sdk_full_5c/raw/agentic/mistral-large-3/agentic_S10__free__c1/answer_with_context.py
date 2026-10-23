import os
from typing import Optional
from model_client import get_llm_client
from model_models import QARequest, QAResponse

def answer_with_context(
    question: str,
    context: str,
    model: str = "anthropic.claude-3-opus-20240229-v1:0"
) -> str:
    """
    Answer a question using provided context with Anthropic's Claude model.
    """
    client = get_llm_client()
    request = QARequest(
        question=question,
        context=context,
        model=model
    )
    response = client.messages.create(
        model=request.model,
        max_tokens=4096,
        messages=[{"role": "user", "content": f"Answer the question using the provided context:\n\nContext: {request.context}\n\nQuestion: {request.question}"}]
    )
    return QAResponse.from_anthropic(response).answer