import os
from typing import Optional
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse

def summarize_text(
    text: str,
    max_length: Optional[int] = 150,
    model: str = "anthropic.claude-3-sonnet-20240229-v1:0"
) -> str:
    """
    Summarize long text using Anthropic's Claude model.
    """
    client = get_llm_client()
    request = SummarizationRequest(
        text=text,
        max_length=max_length,
        model=model
    )
    response = client.messages.create(
        model=request.model,
        max_tokens=request.max_length,
        messages=[{"role": "user", "content": f"Please summarize the following text:\n\n{request.text}"}]
    )
    return SummarizationResponse.from_anthropic(response).summary