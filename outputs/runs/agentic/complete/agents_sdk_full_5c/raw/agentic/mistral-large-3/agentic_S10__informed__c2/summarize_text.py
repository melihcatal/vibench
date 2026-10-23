import os
from typing import Optional
from model_client import get_dashscope_client
from model_models import SummarizationRequest, SummarizationResponse

def summarize_text(
    text: str,
    model: str = "qwen-turbo",
    summary_length: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    """
    Summarize long text using DashScope Qwen model.
    
    Args:
        text: Input text to summarize.
        model: Model identifier (e.g., "qwen-turbo", "qwen-plus").
        summary_length: Optional length constraint (e.g., "short", "medium", "long").
        temperature: Sampling temperature.
    
    Returns:
        Generated summary as a string.
    """
    client = get_dashscope_client()
    
    prompt = f"Summarize the following text:\n\n{text}"
    if summary_length:
        prompt += f"\n\nSummary length: {summary_length}"
    
    request = SummarizationRequest(
        model=model,
        prompt=prompt,
        temperature=temperature,
    )
    
    response = client.call_model(request)
    return SummarizationResponse(**response).output