from typing import Optional, Dict, Any
import os
from model_client import get_llm_client
from model_models import QARequest, QAResponse


def answer_with_context(
    question: str,
    context: str,
    max_tokens: int = 300,
    temperature: float = 0.5,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """
    Answer a question using provided context with OpenAI's gpt-4o-mini model.
    """
    client = get_llm_client(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )

    request = QARequest(
        model=model or "gpt-4o-mini",
        question=question,
        context=context,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt="You are a helpful assistant that answers questions based on the provided context.",
    )

    response = client.create_completion(request)
    return QAResponse(**response).answer
