import os
import google.generativeai as genai
from model_client import get_gemini_model

def answer_with_context(question: str, context: str, model_name: str = "gemini-pro") -> str:
    """
    Calls Google Gemini API to answer a question using provided context.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = get_gemini_model(model_name)
    prompt = f"Given the following context, answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text
