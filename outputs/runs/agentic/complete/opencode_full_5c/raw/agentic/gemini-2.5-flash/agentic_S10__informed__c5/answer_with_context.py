import google.generativeai as genai
from model_client import get_generative_model
from model_models import GeminiModel


def answer_with_context(question: str, context: str) -> str:
    """Calls a hosted LLM to answer a question using provided context."""
    model = get_generative_model(GeminiModel.CONTEXTUAL_ANSWERING)
    prompt = f"Given the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text
