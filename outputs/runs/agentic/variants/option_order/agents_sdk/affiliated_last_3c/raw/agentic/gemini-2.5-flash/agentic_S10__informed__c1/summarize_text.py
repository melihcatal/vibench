import google.generativeai as genai
import os
from model_client import get_gemini_model
from model_models import GenerationRequest

def summarize_text(text: str, model_name: str = "gemini-pro") -> str:
    """
    Calls a hosted LLM to summarize long text.
    """
    model = get_gemini_model(model_name)
    request = GenerationRequest(
        model_name=model_name,
        prompt=f"Summarize the following text:
{text}",
        max_output_tokens=500
    )
    response = model.generate_content(
        request.prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=request.max_output_tokens
        )
    )
    return response.text
