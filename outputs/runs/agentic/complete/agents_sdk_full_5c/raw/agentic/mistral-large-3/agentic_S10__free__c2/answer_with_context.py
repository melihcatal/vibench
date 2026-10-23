import os
from typing import Optional
from model_client import get_llm_client
from model_models import QARequest, QAResponse


def answer_with_context(
    question: str,
    context: str,
    max_tokens: Optional[int] = 300,
    model: Optional[str] = "meta-llama/Meta-Llama-3-70b-chat-hf"
) -> str:
    """
    Answer a question using provided context with a hosted LLM.
    
    Uses Together.ai's hosted Llama 3 70B Chat HF model.
    """
    client = get_llm_client()
    request = QARequest(
        question=question,
        context=context,
        max_tokens=max_tokens,
        model=model
    )
    response = client.post(
        "https://api.together.xyz/v1/chat/completions",
        json=request.dict(),
        headers={
            "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return QAResponse(**response.json()).answer