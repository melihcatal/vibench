import google.generativeai as genai
import os
from model_client import get_gemini_model
from model_models import GenerationRequest

def answer_with_context(question: str, context: str, model_name: str = "gemini-pro") -> str:
    """
    Calls a hosted LLM to answer a question using provided context.
    """
    model = get_gemini_model(model_name)
    prompt = f"Using the following context, answer the question.\nContext: {context}\nQuestion: {question}"
    request = GenerationRequest(
        model_name=model_name,
        prompt=prompt,
        max_output_tokens=500
    )
    response = model.generate_content(
        request.prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=request.max_output_tokens
        )
    )
    return response.text
