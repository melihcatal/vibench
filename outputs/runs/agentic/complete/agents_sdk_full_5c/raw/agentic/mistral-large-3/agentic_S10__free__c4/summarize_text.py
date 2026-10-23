import os
from typing import Optional
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    max_tokens: Optional[int] = 150,
    temperature: Optional[float] = 0.3,
    model: Optional[str] = "gpt-4o-mini"
) -> str:
    """
    Summarize long text using OpenAI's hosted LLM.
    """
    client = get_llm_client()
    request = SummarizationRequest(
        input_text=text,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n\n{request.input_text}"}
        ],
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    return SummarizationResponse.from_openai(response).summary