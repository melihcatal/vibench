import os
import google.generativeai as genai
from model_client import rag_prompt


def answer_with_context(
    question: str, context: str, model: str = "gemini-1.5-pro"
) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model_instance = genai.GenerativeModel(model)
    prompt = rag_prompt(context, question)
    response = model_instance.generate_content(prompt)
    return response.text.strip()
