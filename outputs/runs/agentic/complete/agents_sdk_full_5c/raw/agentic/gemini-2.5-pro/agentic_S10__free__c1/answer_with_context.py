import os
import google.generativeai as genai
from model_client import GOOGLE_API_KEY

def answer_with_context(question: str, context: str) -> str:
    """
    Answers a question based on the provided context using Google's Gemini.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Use the following context to answer the question. If the answer is not in the context, say so.

    Context:
    ---
    {context}
    ---

    Question: {question}
    """

    response = model.generate_content(prompt)
    
    return response.text
