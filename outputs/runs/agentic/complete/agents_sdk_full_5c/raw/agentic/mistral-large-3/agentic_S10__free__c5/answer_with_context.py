import os
from typing import Optional
from model_client import get_llm_client
from model_models import QARequest, QAResponse


def answer_with_context(
    question: str,
    context: str,
    max_tokens: int = 300,
    temperature: float = 0.5,
    model: Optional[str] = "meta-llama/Meta-Llama-3-8B-Instruct"
) -> str:
    """
    Answer a question using provided context with a hosted LLM.
    Uses Together.ai's hosted Llama 3 8B Instruct model by default.
    """
    client = get_llm_client()
    request = QARequest(
        question=question,
        context=context,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model
    )
    response = client.post(
        "/inference",
        json=request.dict(),
        headers={"Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}"}
    )
    response.raise_for_status()
    result = QAResponse(**response.json())
    return result.answer