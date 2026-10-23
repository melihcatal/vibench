import os
from model_client import get_gemini_client
from model_models import LLMResponse

def summarize_text(long_text: str) -> LLMResponse:
    genai = get_gemini_client()
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Please summarize the following text:

{long_text}"
    response = model.generate_content(prompt)
    return LLMResponse(text=response.text)
