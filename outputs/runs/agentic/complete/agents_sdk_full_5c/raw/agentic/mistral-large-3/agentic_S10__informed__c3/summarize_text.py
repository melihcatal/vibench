import os
from typing import Optional
from model_client import get_mistral_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    max_tokens: Optional[int] = 150,
    model: str = "mistral-tiny",
    temperature: float = 0.3
) -> SummarizationResponse:
    """
    Summarize long text using Mistral's hosted LLM.
    """
    client = get_mistral_client()
    request = SummarizationRequest(
        text=text,
        max_tokens=max_tokens,
        model=model,
        temperature=temperature
    )
    
    response = client.chat.complete(
        model=request.model,
        messages=[{"role": "user", "content": f"Summarize the following text:\n\n{request.text}"}],
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    
    return SummarizationResponse(
        summary=response.choices[0].message.content,
        model=response.model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens
    )