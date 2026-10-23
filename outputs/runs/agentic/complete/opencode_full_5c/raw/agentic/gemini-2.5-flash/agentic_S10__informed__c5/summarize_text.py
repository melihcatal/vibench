import google.generativeai as genai
from model_client import get_generative_model
from model_models import GeminiModel


def summarize_text(text: str) -> str:
    """Calls a hosted LLM to summarize long text."""
    model = get_generative_model(GeminiModel.TEXT_SUMMARIZATION)
    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
