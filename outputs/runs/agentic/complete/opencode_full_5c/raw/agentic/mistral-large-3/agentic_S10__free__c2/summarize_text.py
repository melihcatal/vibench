from typing import Optional
from model_client import ModelClient
from model_models import SummarizationRequest


def summarize_text(text: str, max_tokens: int = 150, temperature: float = 0.3) -> str:
    client = ModelClient()
    request = SummarizationRequest(
        text=text, max_tokens=max_tokens, temperature=temperature
    )
    response = client.summarize(request)
    return response.summary
