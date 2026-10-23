import os
from typing import Optional
from model_client import get_llm_client
from model_models import QARequest, QAResponse


def answer_with_context(
    question: str,
    context: str,
    max_tokens: Optional[int] = 150,
    model: Optional[str] = "gpt-4o-mini"
) -> str:
    """
    Answer a question using provided context via OpenAI's hosted LLM.
    """
    client = get_llm_client()
    request = QARequest(
        question=question,
        context=context,
        max_tokens=max_tokens,
        model=model
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant that answers questions using provided context."
            },
            {
                "role": "user", 
                "content": f"Context:\n{request.context}\n\nQuestion: {request.question}"
            }
        ],
        max_tokens=request.max_tokens
    )
    return QAResponse.from_openai(response).answer