import os
from typing import Optional
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    max_tokens: int = 150,
    temperature: float = 0.3,
    model: Optional[str] = "claude-3-sonnet-20240229"
) -> str:
    """
    Summarize long text using Anthropic's Claude model via the Messages API.
    """
    client = get_llm_client()
    
    request = SummarizationRequest(
        prompt=f"Please summarize the following text in a concise manner:\n\n{text}",
        max_tokens=max_tokens,
        temperature=temperature,
        model=model
    )
    
    response = client.messages.create(
        model=request.model,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        messages=[{"role": "user", "content": request.prompt}]
    )
    
    return SummarizationResponse.from_anthropic(response).summary