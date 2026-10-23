import os
import google.generativeai as genai
from model_client import get_gemini_model

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (Google Gemini) to answer a question using provided context.
    """
    model = get_gemini_model("gemini-pro")
    prompt = f"""Using the following context, answer the question.
If the answer is not in the context, state that you don't know.

Context:
{context}

Question:
{question}

Answer:
"""
    response = model.generate_content(prompt)
    return response.text
