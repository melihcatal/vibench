import os
from model_client import get_gemini_client
from model_models import LLMResponse

def summarize_text(text: str, model_id: str = 'gemini-pro') -> LLMResponse:
    client = get_gemini_client()
    prompt = f"Please summarize the following text:\n\n{text}"
    response = client.generate_content(prompt)
    return LLMResponse(text=response.text, raw_response=response.to_dict())

