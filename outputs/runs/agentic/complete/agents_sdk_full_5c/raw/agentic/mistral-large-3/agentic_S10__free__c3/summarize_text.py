import os
from typing import Optional
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse

def summarize_text(text: str, max_length: Optional[int] = 150) -> str:
    """Summarize long text using OpenAI's GPT-4o-mini model."""
    client = get_llm_client()
    request = SummarizationRequest(
        model="gpt-4o-mini",
        text=text,
        max_length=max_length
    )
    response = client.summarize(request)
    return response.summary