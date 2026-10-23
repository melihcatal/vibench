from typing import Optional, Dict, Any
import os
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    max_tokens: int = 150,
    temperature: float = 0.3,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """
    Summarize long text using OpenAI's gpt-4o-mini model.
    """
    client = get_llm_client(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )

    request = SummarizationRequest(
        model=model or "gpt-4o-mini",
        text=text,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt="You are a helpful assistant that summarizes text concisely.",
    )

    response = client.create_completion(request)
    return SummarizationResponse(**response).summary
