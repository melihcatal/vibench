import os
from typing import Optional
from model_client import get_llm_client


def translate_text(
    text: str,
    target_language: str = "es",
    model: Optional[str] = "facebook/m2m100_418M"
) -> str:
    """
    Translate generated model output using Hugging Face's Inference API.
    """
    client = get_llm_client()
    response = client.post(
        f"https://api-inference.huggingface.co/models/{model}",
        json={
            "inputs": text,
            "parameters": {"src_lang": "en", "tgt_lang": target_language}
        },
        headers={
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return response.json()[0]["generated_text"]