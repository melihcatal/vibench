import os
import google.generativeai as genai
from model_client import get_gemini_client


def answer_with_context(question: str, context: str) -> str:
    """
    Calls Google Gemini API to answer a question using provided context.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-pro")
    prompt = f"Using the following context, answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text
