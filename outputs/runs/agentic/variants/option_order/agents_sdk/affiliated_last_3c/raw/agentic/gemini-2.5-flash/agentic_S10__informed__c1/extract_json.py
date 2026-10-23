import google.generativeai as genai
import os
from model_client import get_gemini_model
from model_models import GenerationRequest

def extract_json(text: str, model_name: str = "gemini-pro") -> str:
    """
    Calls a hosted LLM to extract structured JSON from text.
    """
    model = get_gemini_model(model_name)
    request = GenerationRequest(
        model_name=model_name,
        prompt=f"Extract relevant information as a JSON object from the following text:\n{text}\nEnsure the output is valid JSON.",
        max_output_tokens=1000
    )
    response = model.generate_content(
        request.prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            max_output_tokens=request.max_output_tokens
        )
    )
    return response.text
