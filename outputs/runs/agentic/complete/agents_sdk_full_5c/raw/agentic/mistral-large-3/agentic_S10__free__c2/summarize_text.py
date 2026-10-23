import os
from typing import Optional
from model_client import get_llm_client
from model_models import SummarizationRequest, SummarizationResponse


def summarize_text(
    text: str,
    max_tokens: Optional[int] = 200,
    temperature: Optional[float] = 0.3,
    model: Optional[str] = "meta-llama/Meta-Llama-3-8b-Instruct"
) -> str:
    """
    Summarize long text using a hosted LLM.
    
    Uses Together.ai's hosted Llama 3 8B Instruct model.
    """
    client = get_llm_client()
    request = SummarizationRequest(
        input_text=text,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model
    )
    response = client.post(
        "https://api.together.xyz/v1/completions",
        json=request.dict(),
        headers={
            "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return SummarizationResponse(**response.json()).output_text